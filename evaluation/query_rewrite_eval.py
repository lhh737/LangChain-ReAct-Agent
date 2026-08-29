"""
Query Rewrite 消融评估：对比 LLM 改写前后对检索召回的影响

用法：python evaluation/query_rewrite_eval.py

首次运行会用 LLM 改写所有可答题并缓存到 evaluation/query_rewrite_cache.json，
之后运行直接读缓存。报告写入 evaluation/reports/query_rewrite_eval_<timestamp>.md
"""
import sys, os, json
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from rag.bm25_store import BM25Store
from rag.retrieval_strategy import Reranker, HybridScorer, HybridRetriever
from rag.vector_store import VectorStoreService
from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path
from model.factory import chat_model

# ─── 配置 ───
EVAL_PATH = get_abs_path("evaluation/rag_eval_20.jsonl")
CACHE_PATH = get_abs_path("evaluation/query_rewrite_cache.json")
OUTPUT_DIR = get_abs_path("evaluation/reports")
K_VALUES = [5, 10, 20]
RETRIEVAL_K = 50

REWRITE_PROMPT = PromptTemplate.from_template("""\
You are a search query optimizer for an academic paper RAG system. Rewrite the given question into a retrieval-friendly query.

Rules:
1. Expand abbreviations to their full English forms (e.g. DNN→Deep Neural Network, RAG→Retrieval-Augmented Generation, LLM→Large Language Model)
2. KEEP all proper nouns, paper names, and method names EXACTLY as-is (e.g. "PoisonedRAG", "FlatD", "AgentSentinel", "PatchAgent", "CodeLLM-Devkit" — do NOT translate, paraphrase, or abbreviate)
3. Add 2-3 key academic synonyms or related technical terms that appear in paper text
4. Extract core technical noun phrases
5. Output ONLY the rewritten query, no explanation, no quotes, no markdown

Original question: {question}
Rewritten query:""")

ZH_REWRITE_PROMPT = PromptTemplate.from_template("""\
你是一个学术论文 RAG 系统的搜索查询优化器。知识库中的所有论文均为英文，将给定问题改写为更适合检索的查询。

铁律（违反即失败）：
1. 【禁止翻译专有名词】论文名、方法名、系统名、模型名一律保留英文原文！例如 "transformer，CNN，BERT" 等绝对不能翻译成中文
2. 【保留英文缩写】DNN、RAG、LLM 等通用缩写保留英文形式，必要时附加英文全称
3. 添加 2-3 个会出现在英文论文正文中的关键技术英文术语（不是中文翻译）
4. 保持原意不变
5. 只输出改写后的查询，不要解释、引号或 markdown

原始问题：{question}
改写后的查询：""")


# ─── 指标函数（复用 retrieval_eval.py 定义） ───

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

def compute_keyword_coverage_at_k(retrieved, must_contain, k):
    if not must_contain:
        return None
    top_k_text = " ".join(d.page_content for d in retrieved[:k]).lower()
    hits = sum(1 for kw in must_contain if kw.lower() in top_k_text)
    return hits / len(must_contain)

def compute_strict_chunk_recall_at_k(retrieved, expected_chunk_ids, k):
    if not expected_chunk_ids:
        return None
    retrieved_ids = set(d.metadata.get("chunk_id", "") for d in retrieved[:k])
    hits = sum(1 for cid in expected_chunk_ids if cid in retrieved_ids)
    return hits / len(expected_chunk_ids)

def compute_window_chunk_recall_at_k(retrieved, expected_chunk_ids, k, chunk_meta_map):
    if not expected_chunk_ids:
        return None
    retrieved_slice = retrieved[:k]
    hits = 0
    for cid in expected_chunk_ids:
        if any(d.metadata.get("chunk_id", "") == cid for d in retrieved_slice):
            hits += 1
            continue
        exp_meta = chunk_meta_map.get(cid)
        if not exp_meta:
            continue
        for d in retrieved_slice:
            if (d.metadata.get("paper_id") == exp_meta.get("paper_id")
                and d.metadata.get("section") == exp_meta.get("section")
                and abs(d.metadata.get("chunk_index", -1) - exp_meta.get("chunk_index", -1)) <= 1
                and abs(d.metadata.get("page_start", 0) - exp_meta.get("page_start", 0)) <= 1):
                hits += 1
                break
    return hits / len(expected_chunk_ids)

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
    hybrid = HybridRetriever(
        vector_store=vs.vector_store,
        bm25_store=bm25,
        rrf_fusion_k_override=RETRIEVAL_K,
    )
    reranker = Reranker(passage_mode=True, fusion_enabled=True)
    hybrid_scorer = HybridScorer(bm25_store=bm25, reranker=Reranker(passage_mode=True, fusion_enabled=False))
    return vs, bm25, hybrid, reranker, hybrid_scorer


# ─── LLM 改写 ───

def rewrite_questions(questions, force=False):
    """LLM 改写可答题，缓存到 JSON"""
    if os.path.exists(CACHE_PATH) and not force:
        with open(CACHE_PATH, "r") as f:
            cache = json.load(f)
        print(f"加载已有改写缓存：{len(cache)} 条")
        return cache

    cache = {}
    answerable = [q for q in questions if q.get("should_answer") and q.get("expected_chunk_ids")]
    for i, q in enumerate(answerable):
        qid = q["id"]
        query = q["question"]
        lang = detect_lang(qid)
        prompt = ZH_REWRITE_PROMPT if lang == "ZH" else REWRITE_PROMPT
        chain = prompt | chat_model | StrOutputParser()
        try:
            rewritten = chain.invoke({"question": query}).strip().strip('"').strip("'")
            cache[qid] = rewritten
            print(f"[{i+1}/{len(answerable)}] {qid}: {query[:50]}... → {rewritten[:80]}...")
        except Exception as e:
            print(f"[{i+1}/{len(answerable)}] {qid}: ERROR {e}，使用原问题")
            cache[qid] = query

    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    print(f"改写缓存已保存：{len(cache)} 条 → {CACHE_PATH}")
    return cache


# ─── 检索 ───

def retrieve_all_strategies(query, vs, hybrid, reranker, hybrid_scorer, bm25):
    """返回 {strategy_name: list[Document]}"""
    results = {}

    # vector_only
    results["vector_only"] = vs.vector_store.as_retriever(
        search_kwargs={"k": RETRIEVAL_K}
    ).invoke(query)

    # hybrid_no_rerank
    results["hybrid_no_rerank"] = hybrid.retrieve(query, k=RETRIEVAL_K)

    # hybrid_rerank (baseline: passage=True, fusion=True)
    results["hybrid_rerank"] = reranker.rerank(
        query,
        hybrid.retrieve(query, k=50),
        top_k=20,
    )

    # hybrid_score
    results["hybrid_score"] = hybrid_scorer.retrieve(query, bm25_k=50, top_k=20)

    return results


# ─── 主流程 ───

def main():
    # Init
    chunk_meta_map = load_chunk_meta_map()
    print(f"Chunk 元数据：{len(chunk_meta_map)} 条")

    vs, bm25, hybrid, reranker, hybrid_scorer = init_retrievers()

    # Load questions
    with open(EVAL_PATH) as f:
        questions = [json.loads(l) for l in f if l.strip()]

    # Rewrite
    rewrite_cache = rewrite_questions(questions)

    # Only evaluate answerable questions with chunk_ids
    eval_questions = [
        q for q in questions
        if q.get("should_answer") and q.get("expected_chunk_ids")
    ]

    strategies = ["vector_only", "hybrid_no_rerank", "hybrid_rerank", "hybrid_score"]

    # ─── 逐题计算 raw vs rewritten ───
    rows = []
    for q in eval_questions:
        qid = q["id"]
        raw_query = q["question"]
        rewritten_query = rewrite_cache.get(qid, raw_query)

        raw_results = retrieve_all_strategies(raw_query, vs, hybrid, reranker, hybrid_scorer, bm25)
        rw_results = retrieve_all_strategies(rewritten_query, vs, hybrid, reranker, hybrid_scorer, bm25)

        row = {
            "id": qid,
            "raw_query": raw_query,
            "rewritten_query": rewritten_query,
            "answer_type": q.get("answer_type", ""),
            "lang": detect_lang(qid),
            "expected_sources": q.get("expected_sources", []),
            "must_contain": q.get("must_contain", []),
            "expected_chunk_ids": q.get("expected_chunk_ids", []),
            "strategies": {},
        }

        for strat in strategies:
            raw_docs = raw_results[strat]
            rw_docs = rw_results[strat]

            strat_data = {}
            for k in K_VALUES:
                strat_data[f"raw_strict_chunk@{k}"] = compute_strict_chunk_recall_at_k(raw_docs, q["expected_chunk_ids"], k)
                strat_data[f"raw_window_chunk@{k}"] = compute_window_chunk_recall_at_k(raw_docs, q["expected_chunk_ids"], k, chunk_meta_map)
                strat_data[f"raw_source@{k}"] = compute_source_recall_at_k(raw_docs, q["expected_sources"], k)
                strat_data[f"raw_evidence@{k}"] = compute_evidence_recall_at_k(raw_docs, q["expected_sources"], k)
                strat_data[f"raw_keyword@{k}"] = compute_keyword_coverage_at_k(raw_docs, q["must_contain"], k)

                strat_data[f"rw_strict_chunk@{k}"] = compute_strict_chunk_recall_at_k(rw_docs, q["expected_chunk_ids"], k)
                strat_data[f"rw_window_chunk@{k}"] = compute_window_chunk_recall_at_k(rw_docs, q["expected_chunk_ids"], k, chunk_meta_map)
                strat_data[f"rw_source@{k}"] = compute_source_recall_at_k(rw_docs, q["expected_sources"], k)
                strat_data[f"rw_evidence@{k}"] = compute_evidence_recall_at_k(rw_docs, q["expected_sources"], k)
                strat_data[f"rw_keyword@{k}"] = compute_keyword_coverage_at_k(rw_docs, q["must_contain"], k)

            row["strategies"][strat] = strat_data

        rows.append(row)

    # ─── 写报告 ───
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = os.path.join(OUTPUT_DIR, f"query_rewrite_eval_{timestamp}.md")

    with open(output_path, "w", encoding="utf-8") as f:
        w = f.write
        w("# Query Rewrite 消融评估报告\n\n")
        w(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        w(f"**数据集**: `rag_eval_20.jsonl` ({len(eval_questions)} answerable questions)  \n")
        w(f"**评估策略**: {strategies}  \n")
        w(f"**k 值**: {K_VALUES}  \n")
        w(f"**缓存文件**: `query_rewrite_cache.json`\n\n")
        w("---\n\n")

        # ── 1. 改写对照 ──
        w("# 1. 改写前后 Query 对照\n\n")
        w("| ID | Lang | Raw Query | Rewritten Query |\n")
        w("|----|------|-----------|-----------------|\n")
        for r in rows:
            raw_short = r["raw_query"][:80]
            rw_short = r["rewritten_query"][:80]
            w(f"| {r['id']} | {r['lang']} | {raw_short} | {rw_short} |\n")
        w("\n---\n\n")

        # ── 2. 逐题 metric diff（hybrid_score 策略为主） ──
        main_strat = "hybrid_score"
        w(f"# 2. 逐题指标对比（策略：{main_strat}）\n\n")
        for r in rows:
            s = r["strategies"][main_strat]
            w(f"## {r['id']} ({r['answer_type']}, {r['lang']})\n\n")
            w(f"**Raw**: {r['raw_query'][:120]}  \n")
            w(f"**Rewritten**: {r['rewritten_query'][:120]}\n\n")
            w("| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |\n")
            w("|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|\n")
            for k in K_VALUES:
                raw_sc = s.get(f"raw_strict_chunk@{k}") or 0
                rw_sc = s.get(f"rw_strict_chunk@{k}") or 0
                raw_wc = s.get(f"raw_window_chunk@{k}") or 0
                rw_wc = s.get(f"rw_window_chunk@{k}") or 0
                raw_sr = s.get(f"raw_source@{k}") or 0
                rw_sr = s.get(f"rw_source@{k}") or 0
                raw_er = s.get(f"raw_evidence@{k}") or 0
                rw_er = s.get(f"rw_evidence@{k}") or 0
                w(f"| {k} | {raw_sc:.4f} | {rw_sc:.4f} | {rw_sc-raw_sc:+.4f} | "
                  f"{raw_wc:.4f} | {rw_wc:.4f} | {rw_wc-raw_wc:+.4f} | "
                  f"{raw_sr:.4f} | {rw_sr:.4f} | {rw_sr-raw_sr:+.4f} | "
                  f"{raw_er:.4f} | {rw_er:.4f} | {rw_er-raw_er:+.4f} |\n")
            w("\n")

        w("---\n\n")

        # ── 3. 全局汇总（所有策略） ──
        w("# 3. 全局平均指标对比（所有策略）\n\n")
        for strat in strategies:
            w(f"## {strat}\n\n")
            w("| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ | raw keyword | rw keyword | Δ |\n")
            w("|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|---|-------------|---|\n")
            for k in K_VALUES:
                metrics = ["strict_chunk", "window_chunk", "source", "evidence", "keyword"]
                parts = [str(k)]
                for metric in metrics:
                    raw_vals = [r["strategies"][strat].get(f"raw_{metric}@{k}") for r in rows]
                    rw_vals = [r["strategies"][strat].get(f"rw_{metric}@{k}") for r in rows]
                    raw_vals = [v for v in raw_vals if v is not None]
                    rw_vals = [v for v in rw_vals if v is not None]
                    raw_avg = sum(raw_vals) / len(raw_vals) if raw_vals else 0
                    rw_avg = sum(rw_vals) / len(rw_vals) if rw_vals else 0
                    parts.append(f"{raw_avg:.4f} | {rw_avg:.4f} | {rw_avg-raw_avg:+.4f}")
                w("| " + " | ".join(parts) + " |\n")
            w("\n")

        w("---\n\n")

        # ── 4. 按 answer_type 汇总 ──
        w("# 4. 按问题类型汇总（hybrid_score）\n\n")
        type_groups = defaultdict(list)
        for r in rows:
            type_groups[r["answer_type"]].append(r)
        for atype in sorted(type_groups.keys()):
            group = type_groups[atype]
            w(f"## {atype} ({len(group)} questions)\n\n")
            w("| k | raw strict_chunk | rw strict_chunk | Δ | raw evidence | rw evidence | Δ |\n")
            w("|---|-----------------|-----------------|---|--------------|-------------|---|\n")
            for k in K_VALUES:
                raw_sc = [r["strategies"][main_strat].get(f"raw_strict_chunk@{k}") for r in group]
                rw_sc = [r["strategies"][main_strat].get(f"rw_strict_chunk@{k}") for r in group]
                raw_ev = [r["strategies"][main_strat].get(f"raw_evidence@{k}") for r in group]
                rw_ev = [r["strategies"][main_strat].get(f"rw_evidence@{k}") for r in group]
                raw_sc = [v for v in raw_sc if v is not None]
                rw_sc = [v for v in rw_sc if v is not None]
                raw_ev = [v for v in raw_ev if v is not None]
                rw_ev = [v for v in rw_ev if v is not None]
                asc = sum(raw_sc) / len(raw_sc) if raw_sc else 0
                rsc = sum(rw_sc) / len(rw_sc) if rw_sc else 0
                aev = sum(raw_ev) / len(raw_ev) if raw_ev else 0
                rev = sum(rw_ev) / len(rw_ev) if rw_ev else 0
                w(f"| {k} | {asc:.4f} | {rsc:.4f} | {rsc-asc:+.4f} | {aev:.4f} | {rev:.4f} | {rev-aev:+.4f} |\n")
            w("\n")

        w("---\n\n")

        # ── 5. 按语言汇总 ──
        w("# 5. 按语言汇总（hybrid_score）\n\n")
        lang_groups = defaultdict(list)
        for r in rows:
            lang_groups[r["lang"]].append(r)
        for lang in ["EN", "ZH"]:
            group = lang_groups.get(lang, [])
            if not group:
                continue
            w(f"## {lang} ({len(group)} questions)\n\n")
            w("| k | raw strict_chunk | rw strict_chunk | Δ | raw evidence | rw evidence | Δ |\n")
            w("|---|-----------------|-----------------|---|--------------|-------------|---|\n")
            for k in K_VALUES:
                raw_sc = [r["strategies"][main_strat].get(f"raw_strict_chunk@{k}") for r in group]
                rw_sc = [r["strategies"][main_strat].get(f"rw_strict_chunk@{k}") for r in group]
                raw_ev = [r["strategies"][main_strat].get(f"raw_evidence@{k}") for r in group]
                rw_ev = [r["strategies"][main_strat].get(f"rw_evidence@{k}") for r in group]
                raw_sc = [v for v in raw_sc if v is not None]
                rw_sc = [v for v in rw_sc if v is not None]
                raw_ev = [v for v in raw_ev if v is not None]
                rw_ev = [v for v in rw_ev if v is not None]
                asc = sum(raw_sc) / len(raw_sc) if raw_sc else 0
                rsc = sum(rw_sc) / len(rw_sc) if rw_sc else 0
                aev = sum(raw_ev) / len(raw_ev) if raw_ev else 0
                rev = sum(rw_ev) / len(rw_ev) if rw_ev else 0
                w(f"| {k} | {asc:.4f} | {rsc:.4f} | {rsc-asc:+.4f} | {aev:.4f} | {rev:.4f} | {rev-aev:+.4f} |\n")
            w("\n")

    print(f"Report written to: {output_path}")


if __name__ == "__main__":
    main()
