"""
Multi-Query 结构化检索评估：raw vs rewrite vs multi-query 三栏对比

用法：python evaluation/multi_query_eval.py

首次运行用 LLM 生成结构化子查询并缓存到 evaluation/multi_query_cache.json。
报告写入 evaluation/reports/multi_query_eval_<timestamp>.md
"""
import sys, os, json, re
from datetime import datetime
from collections import defaultdict, OrderedDict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from rag.bm25_store import BM25Store
from rag.retrieval_strategy import Reranker, HybridScorer
from rag.vector_store import VectorStoreService
from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path
from model.factory import chat_model, _get_chat_model

# ─── 配置 ───
EVAL_PATH = get_abs_path("evaluation/rag_eval_20.jsonl")
REWRITE_CACHE_PATH = get_abs_path("evaluation/query_rewrite_cache.json")
MULTI_CACHE_PATH = get_abs_path("evaluation/multi_query_cache.json")
ZH_TRANSLATE_CACHE_PATH = get_abs_path("evaluation/zh_translate_cache.json")
OUTPUT_DIR = get_abs_path("evaluation/reports")
K_VALUES = [5, 10, 20]

# Multi-Query 配额参数
PER_ENTITY_BM25_K = 15
PER_ENTITY_VEC_K = 5
MIN_PER_ENTITY = 3
TOTAL_TOP_K = 50

# LLM 结构化输出的 Prompt
MULTI_QUERY_PROMPT = PromptTemplate.from_template("""\
You are a retrieval query planner for an academic paper RAG system. Given a question, output a structured JSON plan.

Rules:
1. Identify all paper names / method names / system names mentioned in the question as "entities"
2. For COMPARISON questions (comparing multiple papers): create one subquery per entity, targeting that entity's contribution
3. For SINGLE-PAPER questions: create 2-3 subqueries from different semantic angles (architecture, method details, evaluation, etc.)
4. Each subquery MUST include the entity name verbatim and use English academic terminology
5. Keep original proper nouns, paper names, system names EXACTLY as-is — never translate them
6. Each subquery under 80 characters

Output ONLY valid JSON, no markdown, no explanation:
{{
  "query_type": "comparison" or "single",
  "entities": ["Entity1", "Entity2"],
  "subqueries": [
    {{"entity": "Entity1", "query": "Entity1 specific retrieval query ..."}},
    {{"entity": "Entity2", "query": "Entity2 specific retrieval query ..."}}
  ]
}}

Question: {question}
JSON:""")

ZH_MULTI_QUERY_PROMPT = PromptTemplate.from_template("""\
你是一个学术论文 RAG 系统的检索查询规划器。给定一个中文问题，输出结构化的 JSON 检索计划。

规则：
1. 从问题中识别所有论文名、方法名、系统名作为 "entities"（保留英文原文，绝对不能翻译）
2. 比较类问题：每个实体生成一个子查询，针对该实体的具体贡献
3. 单论文问题：从不同语义角度生成 2-3 个子查询（如架构、方法细节、实验评估等）
4. 每个子查询必须包含实体的英文原名，使用英文学术术语（知识库是全英文的）
5. 每个子查询不超过 80 字符
6. 专有名词必须保留英文原文

只输出合法的 JSON，不要 markdown，不要解释：
{{
  "query_type": "comparison" or "single",
  "entities": ["Entity1", "Entity2"],
  "subqueries": [
    {{"entity": "Entity1", "query": "Entity1 specific retrieval query ..."}},
    {{"entity": "Entity2", "query": "Entity2 specific retrieval query ..."}}
  ]
}}

问题：{question}
JSON：""")

# ─── 语言检测 + 中→英 翻译 Prompt（hybrid_rerank_translate 策略） ───

DETECT_TRANSLATE_PROMPT = PromptTemplate.from_template("""\
You are a query language detector and translator for an English-only academic paper retrieval system.

If the query is already in English, output it EXACTLY unchanged — do NOT modify, improve, or rewrite a single character.
If the query is in Chinese (or any non-English language), translate it into English following these rules:

1. NEVER translate proper nouns — paper names, method names, system names, model names MUST stay in their original English form (e.g., "transformer", "CNN", "BERT", "BTD", "PoisonedRAG", "FlippedRAG", "AgentSentinel")
2. Keep abbreviations in English (DNN, RAG, LLM, NLP, etc.), optionally append their English full names
3. Preserve the original meaning exactly

Output ONLY the resulting query. No explanation, no quotes, no markdown.

Query: {query}
Output:""")

# ─── 中→英 翻译（带头文件缓存） ───

def _load_zh_translate_cache() -> dict:
    if os.path.exists(ZH_TRANSLATE_CACHE_PATH):
        with open(ZH_TRANSLATE_CACHE_PATH, "r") as f:
            return json.load(f)
    return {}

def _save_zh_translate_cache(cache: dict):
    with open(ZH_TRANSLATE_CACHE_PATH, "w") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def _translate_zh_query(query: str, cache: dict) -> str:
    """LLM 自动检测语言：英文→原样返回，中文→翻译为英文学术检索词（缓存命中则跳过 LLM）"""
    if query in cache:
        return cache[query]
    try:
        chain = DETECT_TRANSLATE_PROMPT | _get_chat_model() | StrOutputParser()
        result = chain.invoke({"query": query}).strip()
        result = result.strip('"').strip("'").strip()
        cache[query] = result
        return result
    except Exception as e:
        print(f"  [detect+translate] LLM 失败：{e}，回退原文")
        cache[query] = query
        return query


# ─── 指标函数 ───

def doc_matches_source(doc, filename_fragment):
    return filename_fragment.lower() in (doc.metadata.get("source_file", "") or "").lower()

def doc_matches_source_and_page(doc, fn, pages):
    if not fn:
        return False
    if not doc_matches_source(doc, fn):
        return False
    if not pages:
        return True
    ps = doc.metadata.get("page_start")
    pe = doc.metadata.get("page_end")
    if ps is None:
        return doc.metadata.get("page") in pages
    return any(int(ps) <= p <= int(pe) for p in pages)

def compute_source_recall_at_k(retrieved, expected_sources, k):
    if not expected_sources:
        return None
    top_k = retrieved[:k]
    hit = set()
    for es in expected_sources:
        fn = es.get("filename_contains", "")
        if not fn:
            continue
        for doc in top_k:
            if doc_matches_source(doc, fn):
                hit.add(fn.lower())
                break
    return len(hit) / len(expected_sources)

def compute_evidence_recall_at_k(retrieved, expected_sources, k):
    if not expected_sources:
        return None
    top_k = retrieved[:k]
    hit = 0
    for es in expected_sources:
        fn = es.get("filename_contains", "")
        pages = es.get("pages_any", [])
        if not fn:
            continue
        for doc in top_k:
            if doc_matches_source_and_page(doc, fn, pages):
                hit += 1
                break
    return hit / len(expected_sources)

def _normalize_chunk_groups(expected_chunk_ids):
    """统一 flat/groups 格式 → list[list[str]]。
    flat:   ["cid1", "cid2"]          → [["cid1"], ["cid2"]]
    grouped: [["cid1"], ["cid2","cid3"]] → 原样返回
    """
    if not expected_chunk_ids:
        return []
    if isinstance(expected_chunk_ids[0], list):
        return expected_chunk_ids
    return [[cid] for cid in expected_chunk_ids]


def compute_strict_chunk_recall_at_k(retrieved, expected_chunk_ids, k):
    groups = _normalize_chunk_groups(expected_chunk_ids)
    if not groups:
        return None
    retrieved_ids = set(d.metadata.get("chunk_id", "") for d in retrieved[:k])
    hits = sum(1 for group in groups if any(cid in retrieved_ids for cid in group))
    return hits / len(groups)

def compute_window_chunk_recall_at_k(retrieved, expected_chunk_ids, k, chunk_meta_map):
    groups = _normalize_chunk_groups(expected_chunk_ids)
    if not groups:
        return None
    retrieved_slice = retrieved[:k]
    hits = 0
    for group in groups:
        # strict: group 内任一 cid 精确命中
        if any(d.metadata.get("chunk_id", "") in group for d in retrieved_slice):
            hits += 1
            continue
        # window: 对 group 内每个 cid 尝试窗口匹配
        window_hit = False
        for cid in group:
            exp_meta = chunk_meta_map.get(cid)
            if not exp_meta:
                continue
            for d in retrieved_slice:
                if (d.metadata.get("paper_id") == exp_meta.get("paper_id")
                    and d.metadata.get("section") == exp_meta.get("section")
                    and abs(d.metadata.get("chunk_index", -1) - exp_meta.get("chunk_index", -1)) <= 1
                    and abs(d.metadata.get("page_start", 0) - exp_meta.get("page_start", 0)) <= 1):
                    window_hit = True
                    break
            if window_hit:
                break
        if window_hit:
            hits += 1
    return hits / len(groups)

def compute_keyword_coverage_at_k(retrieved, must_contain, k):
    if not must_contain:
        return None
    top_k_text = " ".join(d.page_content for d in retrieved[:k]).lower()
    hits = sum(1 for kw in must_contain if kw.lower() in top_k_text)
    return hits / len(must_contain)

def detect_lang(qid):
    return "ZH" if qid.endswith("_zh") else "EN"


# ─── 初始化 ───

def load_chunk_meta_map():
    client = chromadb.PersistentClient(path=get_abs_path("chroma_db"))
    collection = client.get_collection(chroma_conf["collection_name"])
    all_data = collection.get(include=["metadatas"], limit=5000)
    return {m["chunk_id"]: m for m in all_data["metadatas"] if m.get("chunk_id")}

def init_retrievers():
    vs = VectorStoreService()
    bm25 = BM25Store()
    bm25.load()
    bm25.add_domain_terms()
    hyb_scorer = HybridScorer(bm25_store=bm25, reranker=Reranker(passage_mode=True, fusion_enabled=False))
    return vs, bm25, hyb_scorer


# ─── Multi-Query 检索引擎 ───

def multi_query_retrieve(subqueries, bm25, vs, hyb_scorer):
    """Per-entity quota 检索合并

    subqueries: [{"entity": "...", "query": "..."}, ...]
    返回: list[Document] (TOTAL_TOP_K 个，满足 MIN_PER_ENTITY)
    """
    # 按 entity 分组收集
    entity_docs: dict[str, OrderedDict[str, Document]] = defaultdict(OrderedDict)
    # entity_docs[entity][chunk_id] = Document (去重用)

    for sq in subqueries:
        entity = sq["entity"]
        query = sq["query"]

        # BM25 top-PER_ENTITY_BM25_K
        try:
            bm25_results = bm25.search(query, PER_ENTITY_BM25_K)
            for d, score in bm25_results:
                cid = d.metadata.get("chunk_id", "")
                if cid and cid not in entity_docs[entity]:
                    # Attach BM25 score to metadata for sorting
                    d.metadata["_bm25_score"] = score
                    entity_docs[entity][cid] = d
        except Exception:
            pass

        # Vector top-PER_ENTITY_VEC_K
        try:
            vector_docs = vs.vector_store.as_retriever(
                search_kwargs={"k": PER_ENTITY_VEC_K}
            ).invoke(query)
            for d in vector_docs:
                cid = d.metadata.get("chunk_id", "")
                if cid and cid not in entity_docs[entity]:
                    d.metadata["_bm25_score"] = 0.0
                    entity_docs[entity][cid] = d
        except Exception:
            pass

    # 每 entity 内部按 BM25 score 排序
    for entity in entity_docs:
        sorted_docs = sorted(
            entity_docs[entity].values(),
            key=lambda d: d.metadata.get("_bm25_score", 0),
            reverse=True,
        )
        entity_docs[entity] = OrderedDict((d.metadata.get("chunk_id", ""), d) for d in sorted_docs)

    # Round-robin 合并，确保每 entity ≥ MIN_PER_ENTITY
    entities = list(entity_docs.keys())
    entity_iters = {e: iter(entity_docs[e].values()) for e in entities}
    entity_counts = {e: 0 for e in entities}

    merged: list[Document] = []
    seen_ids: set[str] = set()

    # Phase 1: 轮流从每实体取 1 个，直到满足 MIN_PER_ENTITY
    while any(entity_counts[e] < MIN_PER_ENTITY for e in entities) and len(merged) < TOTAL_TOP_K:
        for e in entities:
            if entity_counts[e] >= MIN_PER_ENTITY:
                continue
            try:
                doc = next(entity_iters[e])
                cid = doc.metadata.get("chunk_id", "")
                if cid not in seen_ids:
                    merged.append(doc)
                    seen_ids.add(cid)
                    entity_counts[e] += 1
            except StopIteration:
                entity_counts[e] = max(entity_counts[e], MIN_PER_ENTITY)  # 标记已完成

    # Phase 2: 继续 round-robin 填充到 TOTAL_TOP_K
    while len(merged) < TOTAL_TOP_K:
        added = False
        for e in entities:
            if len(merged) >= TOTAL_TOP_K:
                break
            try:
                doc = next(entity_iters[e])
                cid = doc.metadata.get("chunk_id", "")
                if cid not in seen_ids:
                    merged.append(doc)
                    seen_ids.add(cid)
                    added = True
            except StopIteration:
                pass
        if not added:
            break

    return merged[:TOTAL_TOP_K]


# ─── LLM 生成结构化查询 ───

def generate_multi_queries(questions, force=False):
    if os.path.exists(MULTI_CACHE_PATH) and not force:
        with open(MULTI_CACHE_PATH, "r") as f:
            cache = json.load(f)
        print(f"加载 Multi-Query 缓存：{len(cache)} 条")
        return cache

    cache = {}
    answerable = [q for q in questions if q.get("should_answer") and _normalize_chunk_groups(q.get("expected_chunk_ids", []))]
    for i, q in enumerate(answerable):
        qid = q["id"]
        query = q["question"]
        lang = detect_lang(qid)
        prompt = ZH_MULTI_QUERY_PROMPT if lang == "ZH" else MULTI_QUERY_PROMPT
        chain = prompt | chat_model | StrOutputParser()

        try:
            raw_output = chain.invoke({"question": query}).strip()
            # 清洗：去掉可能的 markdown 代码块包装
            raw_output = re.sub(r'^```(?:json)?\s*', '', raw_output)
            raw_output = re.sub(r'\s*```$', '', raw_output)
            parsed = json.loads(raw_output)
            cache[qid] = {
                "query_type": parsed.get("query_type", "single"),
                "entities": parsed.get("entities", []),
                "subqueries": parsed.get("subqueries", []),
            }
            print(f"[{i+1}/{len(answerable)}] {qid}: {parsed.get('query_type')} "
                  f"entities={parsed.get('entities')} subqueries={len(parsed.get('subqueries',[]))}")
        except Exception as e:
            print(f"[{i+1}/{len(answerable)}] {qid}: JSON parse ERROR — {e}")
            print(f"  Raw output: {raw_output[:200]}")
            # Fallback: single query
            cache[qid] = {
                "query_type": "single",
                "entities": ["fallback"],
                "subqueries": [{"entity": "fallback", "query": query}],
            }

    with open(MULTI_CACHE_PATH, "w") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    print(f"Multi-Query 缓存已保存：{len(cache)} 条 → {MULTI_CACHE_PATH}")
    return cache


# ─── 主流程 ───

def main():
    chunk_meta_map = load_chunk_meta_map()
    print(f"Chunk 元数据：{len(chunk_meta_map)} 条")

    vs, bm25, hyb_scorer = init_retrievers()

    # Load
    with open(EVAL_PATH) as f:
        questions = [json.loads(l) for l in f if l.strip()]

    rewrite_cache = {}
    if os.path.exists(REWRITE_CACHE_PATH):
        with open(REWRITE_CACHE_PATH) as f:
            rewrite_cache = json.load(f)

    multi_cache = generate_multi_queries(questions)

    zh_translate_cache = _load_zh_translate_cache()

    eval_questions = [q for q in questions if q.get("should_answer") and _normalize_chunk_groups(q.get("expected_chunk_ids", []))]

    # 预检测+翻译全部题目（LLM 自动判断语言，英文原样返回）
    tr_count = 0
    for q in eval_questions:
        result = _translate_zh_query(q["question"], zh_translate_cache)
        if result != q["question"]:
            tr_count += 1
    if tr_count:
        _save_zh_translate_cache(zh_translate_cache)
    print(f"语言检测+翻译：{tr_count} 题需要翻译（共 {len(eval_questions)} 题）")

    # ─── 逐题三栏对比 ───
    rows = []
    for q in eval_questions:
        qid = q["id"]
        raw_query = q["question"]
        rw_query = rewrite_cache.get(qid, raw_query)
        mq_plan = multi_cache.get(qid, {"subqueries": [{"entity": "fallback", "query": raw_query}]})

        # raw
        raw_docs = hyb_scorer.retrieve(raw_query, bm25_k=50, top_k=50)
        # rewrite
        rw_docs = hyb_scorer.retrieve(rw_query, bm25_k=50, top_k=50)
        # translate: LLM 检测语言，中文翻译英文，英文原样
        tr_query = zh_translate_cache.get(raw_query, raw_query)
        tr_docs = hyb_scorer.retrieve(tr_query, bm25_k=50, top_k=50)
        # multi-query: 构建 pool（per-entity 覆盖）→ 三种 Fusion 打分
        mq_pool = multi_query_retrieve(mq_plan["subqueries"], bm25, vs, hyb_scorer)
        mq_zscore_docs: list = []
        mq_rawmax_docs: list = []
        mq_rrf_docs: list = []
        if mq_pool:
            try:
                # ── Phase 2: Per-Subquery 独立打分（三种 Fusion 共享） ──
                all_subq_scores: list[dict[int, float]] = []
                all_subq_bm25: list[dict[int, float]] = []

                for sq in mq_plan["subqueries"]:
                    sq_query = sq["query"]
                    sq_bm25_raw = bm25.search(sq_query, k=200)
                    cid_to_bm25 = {d.metadata.get("chunk_id", ""): s for d, s in sq_bm25_raw}
                    sq_rerank = hyb_scorer.reranker.score_batch(sq_query, mq_pool)

                    sq_scores = {}
                    sq_bm25_scores = {}
                    for i, d in enumerate(mq_pool):
                        cid = d.metadata.get("chunk_id", "")
                        bm25_s = cid_to_bm25.get(cid, 0.0)
                        rerank_s = sq_rerank.get(i, 0.0)
                        kw_s = hyb_scorer._keyword_overlap(sq_query, d.page_content)
                        meta_s = hyb_scorer._metadata_boost(sq_query, d)
                        sq_scores[i] = (
                            hyb_scorer.w_bm25 * bm25_s
                            + hyb_scorer.w_rerank * rerank_s
                            + hyb_scorer.w_keyword * kw_s
                            + hyb_scorer.w_metadata * meta_s
                        )
                        sq_bm25_scores[i] = bm25_s
                    all_subq_scores.append(sq_scores)
                    all_subq_bm25.append(sq_bm25_scores)

                # ── 通用 helper: 排序 + BM25 保底 → top-K docs ──
                def _select_with_bm25_safeguard(
                    final_scores: dict[int, float],
                    bm25_max: dict[int, float],
                    top_k: int = 50,
                ) -> list:
                    ranking = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
                    bm25_top5 = {i for i, _ in sorted(bm25_max.items(), key=lambda x: x[1], reverse=True)[:5]}
                    docs = []
                    seen = set()
                    for i, _ in ranking:
                        if len(docs) >= top_k:
                            break
                        if i not in seen:
                            docs.append(mq_pool[i])
                            seen.add(i)
                    for i in sorted(bm25_top5):
                        if i not in seen and len(docs) < top_k:
                            docs.append(mq_pool[i])
                    return docs

                N = len(mq_pool)

                # ── 变体 1: Z-Score Max-Fusion（当前 mq） ──
                def _zscore_norm(scores: dict[int, float]) -> dict[int, float]:
                    vals = list(scores.values())
                    mean_s = sum(vals) / len(vals)
                    var_s = sum((v - mean_s) ** 2 for v in vals) / len(vals)
                    std_s = var_s ** 0.5
                    if std_s < 1e-8:
                        std_s = 1.0
                    return {i: (s - mean_s) / std_s for i, s in scores.items()}

                zscore_final = {i: max(_zscore_norm(sqs)[i] for sqs in all_subq_scores) for i in range(N)}
                zscore_bm25 = {i: max(_zscore_norm(bs)[i] for bs in all_subq_bm25) for i in range(N)}
                mq_zscore_docs = _select_with_bm25_safeguard(zscore_final, zscore_bm25)

                # ── 变体 2: Raw Max-Fusion（方案 A，不做标准化） ──
                rawmax_final = {i: max(sqs[i] for sqs in all_subq_scores) for i in range(N)}
                rawmax_bm25 = {i: max(bs[i] for bs in all_subq_bm25) for i in range(N)}
                mq_rawmax_docs = _select_with_bm25_safeguard(rawmax_final, rawmax_bm25)

                # ── 变体 3: RRF Fusion（方案 B，纯排名融合 + BM25 保底） ──
                RRF_K = 60
                rrf_scores: dict[int, float] = {}
                for sq_scores in all_subq_scores:
                    ranked = sorted(sq_scores.items(), key=lambda x: x[1], reverse=True)
                    for rank, (i, _) in enumerate(ranked, 1):
                        rrf_scores[i] = rrf_scores.get(i, 0) + 1.0 / (RRF_K + rank)
                rrf_bm25_max = {i: max(bs[i] for bs in all_subq_bm25) for i in range(N)}
                mq_rrf_docs = _select_with_bm25_safeguard(rrf_scores, rrf_bm25_max)

            except Exception:
                mq_zscore_docs = mq_pool[:50]
                mq_rawmax_docs = mq_pool[:50]
                mq_rrf_docs = mq_pool[:50]
        else:
            mq_zscore_docs = []
            mq_rawmax_docs = []
            mq_rrf_docs = []

        row = {
            "id": qid,
            "raw_query": raw_query,
            "rewritten_query": rw_query,
            "translated_query": zh_translate_cache.get(raw_query, raw_query),
            "multi_plan": mq_plan,
            "answer_type": q.get("answer_type", ""),
            "lang": detect_lang(qid),
            "expected_sources": q.get("expected_sources", []),
            "must_contain": q.get("must_contain", []),
            "expected_chunk_ids": q.get("expected_chunk_ids", []),
        }

        for label, docs in [("raw", raw_docs), ("rw", rw_docs),
                             ("tr", tr_docs),
                             ("mq_zscore", mq_zscore_docs),
                             ("mq_rawmax", mq_rawmax_docs),
                             ("mq_rrf", mq_rrf_docs)]:
            for k in K_VALUES:
                row[f"{label}_strict_chunk@{k}"] = compute_strict_chunk_recall_at_k(docs, q["expected_chunk_ids"], k)
                row[f"{label}_window_chunk@{k}"] = compute_window_chunk_recall_at_k(docs, q["expected_chunk_ids"], k, chunk_meta_map)
                row[f"{label}_source@{k}"] = compute_source_recall_at_k(docs, q["expected_sources"], k)
                row[f"{label}_evidence@{k}"] = compute_evidence_recall_at_k(docs, q["expected_sources"], k)
                row[f"{label}_keyword@{k}"] = compute_keyword_coverage_at_k(docs, q["must_contain"], k)

            # entity coverage
            entity_hits = set()
            for d in docs:
                for es in q["expected_sources"]:
                    fn = es.get("filename_contains", "")
                    if fn and doc_matches_source(d, fn):
                        entity_hits.add(fn.lower())
            row[f"{label}_entity_coverage"] = len(entity_hits) / len(q["expected_sources"]) if q["expected_sources"] else None

        rows.append(row)

    # ─── 写报告 ───
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = os.path.join(OUTPUT_DIR, f"multi_query_eval_{timestamp}.md")

    with open(output_path, "w", encoding="utf-8") as f:
        w = f.write
        w("# Multi-Query 结构化检索评估报告\n\n")
        w(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        w(f"**数据集**: `rag_eval_20.jsonl` ({len(eval_questions)} answerable questions)  \n")
        w(f"**策略**: raw vs rewrite vs translate vs mq_zscore vs mq_rawmax vs mq_rrf  \n")
        w(f"**Multi-Query 配额**: per-entity BM25={PER_ENTITY_BM25_K}, Vector={PER_ENTITY_VEC_K}, min={MIN_PER_ENTITY}, total={TOTAL_TOP_K}  \n")
        w(f"**k 值**: {K_VALUES}  \n\n")
        w("---\n\n")

        # ── 1. Multi-Query 计划展示 ──
        w("# 1. Multi-Query 结构化计划\n\n")
        for r in rows:
            plan = r["multi_plan"]
            w(f"## {r['id']} ({r['answer_type']}, {r['lang']})\n\n")
            w(f"**原问题**: {r['raw_query'][:100]}  \n")
            w(f"**类型**: {plan.get('query_type')} | **实体**: {plan.get('entities')}\n\n")
            w("| # | Entity | Sub-query |\n")
            w("|---|--------|----------|\n")
            for i, sq in enumerate(plan.get("subqueries", []), 1):
                w(f"| {i} | {sq['entity']} | {sq['query']} |\n")
            w("\n")

        w("---\n\n")

        # ── 2. 逐题五栏对比 ──
        w("# 2. 逐题指标对比（raw vs rewrite vs translate vs mq_zscore vs mq_rawmax vs mq_rrf）\n\n")
        MQ_LABELS = ["mq_zscore", "mq_rawmax", "mq_rrf"]
        for r in rows:
            w(f"## {r['id']} ({r['answer_type']}, {r['lang']})\n\n")
            w(f"**Raw**: {r['raw_query'][:120]}  \n")
            w(f"**Rewritten**: {r['rewritten_query'][:120]}  \n")
            w(f"**Translated**: {r['translated_query'][:120]}  \n")
            subq_preview = " | ".join(sq["query"][:60] for sq in r["multi_plan"].get("subqueries", []))
            w(f"**Multi-Query**: {subq_preview[:200]}\n\n")

            # strict chunk recall: 6 策略
            w("| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |\n")
            w("|---|-----|----|----|----------|----------|--------|\n")
            for k in K_VALUES:
                vals = [r.get(f"{lb}_strict_chunk@{k}") or 0 for lb in ["raw", "rw", "tr"] + MQ_LABELS]
                w("| " + " | ".join([str(k)] + [f"{v:.4f}" for v in vals]) + " |\n")

            # window chunk recall
            w("\n| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |\n")
            w("|---|-----------|----------|----------|-----------------|-----------------|---------------|\n")
            for k in K_VALUES:
                vals = [r.get(f"{lb}_window_chunk@{k}") or 0 for lb in ["raw", "rw", "tr"] + MQ_LABELS]
                w("| " + " | ".join([str(k)] + [f"{v:.4f}" for v in vals]) + " |\n")

            # source + evidence
            w("\n| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |\n")
            w("|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|\n")
            for k in K_VALUES:
                parts = [k]
                for lb in ["raw", "rw", "tr"] + MQ_LABELS:
                    parts.append(r.get(f"{lb}_source@{k}") or 0)
                for lb in ["raw", "rw", "tr"] + MQ_LABELS:
                    parts.append(r.get(f"{lb}_evidence@{k}") or 0)
                w("| " + " | ".join(f"{v:.4f}" if isinstance(v, float) else str(v) for v in parts) + " |\n")

            # Entity coverage
            covs = " | ".join(f"{lb}={r.get(f'{lb}_entity_coverage',0) or 0:.2f}"
                             for lb in ["raw", "rw", "tr"] + MQ_LABELS)
            w(f"\n**Entity Coverage**: {covs}\n\n")

        w("---\n\n")

        # ── 3. 全局汇总 ──
        w("# 3. 全局平均指标对比\n\n")
        ALL_LABELS = ["raw", "rw", "tr"] + MQ_LABELS
        LABEL_NAMES = {"raw": "Raw Query", "rw": "Query Rewrite",
                       "tr": "ZH→EN Translate + HybridScorer",
                       "mq_zscore": "MQ Z-Score Max-Fusion",
                       "mq_rawmax": "MQ Raw Max-Fusion (方案A)",
                       "mq_rrf": "MQ RRF Fusion (方案B)"}

        for label in ALL_LABELS:
            w(f"## {LABEL_NAMES[label]}\n\n")
            w("| k | strict_chunk | window_chunk | source | evidence |\n")
            w("|---|-------------|-------------|--------|----------|\n")
            for k in K_VALUES:
                sc = [r.get(f"{label}_strict_chunk@{k}") for r in rows]
                wc = [r.get(f"{label}_window_chunk@{k}") for r in rows]
                sr = [r.get(f"{label}_source@{k}") for r in rows]
                er = [r.get(f"{label}_evidence@{k}") for r in rows]
                sc_v = [v for v in sc if v is not None]
                wc_v = [v for v in wc if v is not None]
                sr_v = [v for v in sr if v is not None]
                er_v = [v for v in er if v is not None]
                w(f"| {k} | {sum(sc_v)/len(sc_v):.4f} | {sum(wc_v)/len(wc_v):.4f} | {sum(sr_v)/len(sr_v):.4f} | {sum(er_v)/len(er_v):.4f} |\n")
            w("\n")

        # Diff table: raw vs all variants
        w("## Raw → Rewrite → Translate → MQ Variants 变化（strict_chunk）\n\n")
        header = "| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |"
        sep = "|---|-----|----|----|----------|----------|--------|"
        for suffix, delta_target in [("", ""), (" raw→rw", "rw"), (" raw→tr", "tr"),
                                       (" raw→zscore", "mq_zscore"),
                                       (" raw→rawmax", "mq_rawmax"), (" raw→rrf", "mq_rrf")]:
            if suffix:
                w(f"\n### Delta vs Raw{suffix}\n\n")
                w("| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf | raw→rw | raw→tr | raw→zscore | raw→rawmax | raw→rrf |\n")
                w("|---|-----|----|----|----------|----------|--------|--------|--------|-----------|-----------|---------|\n")
                for k in K_VALUES:
                    means = {}
                    for lb in ALL_LABELS:
                        vals = [r.get(f"{lb}_strict_chunk@{k}") for r in rows]
                        vals = [v for v in vals if v is not None]
                        means[lb] = sum(vals)/len(vals) if vals else 0
                    w(f"| {k} | {means['raw']:.4f} | {means['rw']:.4f} | {means['tr']:.4f} | {means['mq_zscore']:.4f} | "
                      f"{means['mq_rawmax']:.4f} | {means['mq_rrf']:.4f} | "
                      f"{means['rw']-means['raw']:+.4f} | {means['tr']-means['raw']:+.4f} | "
                      f"{means['mq_zscore']-means['raw']:+.4f} | "
                      f"{means['mq_rawmax']-means['raw']:+.4f} | {means['mq_rrf']-means['raw']:+.4f} |\n")
            else:
                w("\n### 绝对值\n\n")
                w("| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |\n")
                w("|---|-----|----|----|----------|----------|--------|\n")
                for k in K_VALUES:
                    means = {}
                    for lb in ALL_LABELS:
                        vals = [r.get(f"{lb}_strict_chunk@{k}") for r in rows]
                        vals = [v for v in vals if v is not None]
                        means[lb] = sum(vals)/len(vals) if vals else 0
                    w(f"| {k} | {means['raw']:.4f} | {means['rw']:.4f} | {means['tr']:.4f} | {means['mq_zscore']:.4f} | "
                      f"{means['mq_rawmax']:.4f} | {means['mq_rrf']:.4f} |\n")
        w("\n")

        w("---\n\n")

        # ── 4. 按问题类型汇总 ──
        w("# 4. 按问题类型汇总（strict_chunk）\n\n")
        type_groups = defaultdict(list)
        for r in rows:
            type_groups[r["answer_type"]].append(r)
        for atype in sorted(type_groups.keys()):
            group = type_groups[atype]
            w(f"## {atype} ({len(group)} questions)\n\n")
            w("| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |\n")
            w("|---|-----|----|----|----------|----------|--------|\n")
            for k in K_VALUES:
                means = {}
                for lb in ALL_LABELS:
                    vals = [r.get(f"{lb}_strict_chunk@{k}") for r in group]
                    vals = [v for v in vals if v is not None]
                    means[lb] = sum(vals)/len(vals) if vals else 0
                w(f"| {k} | {means['raw']:.4f} | {means['rw']:.4f} | {means['mq_zscore']:.4f} | "
                  f"{means['mq_rawmax']:.4f} | {means['mq_rrf']:.4f} |\n")
            w("\n")

        w("---\n\n")

        # ── 5. 按语言汇总 ──
        w("# 5. 按语言汇总（strict_chunk）\n\n")
        lang_groups = defaultdict(list)
        for r in rows:
            lang_groups[r["lang"]].append(r)
        for lang in ["EN", "ZH"]:
            group = lang_groups.get(lang, [])
            if not group:
                continue
            w(f"## {lang} ({len(group)} questions)\n\n")
            w("| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |\n")
            w("|---|-----|----|----|----------|----------|--------|\n")
            for k in K_VALUES:
                means = {}
                for lb in ALL_LABELS:
                    vals = [r.get(f"{lb}_strict_chunk@{k}") for r in group]
                    vals = [v for v in vals if v is not None]
                    means[lb] = sum(vals)/len(vals) if vals else 0
                w(f"| {k} | {means['raw']:.4f} | {means['rw']:.4f} | {means['mq_zscore']:.4f} | "
                  f"{means['mq_rawmax']:.4f} | {means['mq_rrf']:.4f} |\n")
            w("\n")

    print(f"Report written to: {output_path}")


if __name__ == "__main__":
    main()
