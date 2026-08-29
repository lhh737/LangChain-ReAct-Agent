"""
检索策略消融评估 v3
指标：Source Recall@k / Evidence Recall@k / Source Hit@k / All Sources Hit@k /
       Source MRR / Keyword Coverage@k / Strict Chunk Recall@k / Window Chunk Recall@k
新增：分阶段召回统计 / RRF-K 消融 / metadata boost 对比
should_answer=false 的题排除在检索均值外，单独统计
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from datetime import datetime
from collections import defaultdict

import chromadb
from langchain_core.documents import Document
from rag.vector_store import VectorStoreService
from rag.bm25_store import BM25Store
from rag.retrieval_strategy import HybridRetriever, Reranker, HybridScorer
from rag.rag_service import RagSummarizeService
from evaluation.multi_query_eval import multi_query_retrieve, _translate_zh_query, _load_zh_translate_cache
from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

CHUNK_EVAL_PATH = get_abs_path("evaluation/rag_eval_20.jsonl")
MULTI_CACHE_PATH = get_abs_path("evaluation/multi_query_cache.json")
REPORT_DIR = get_abs_path("evaluation/reports")

K_VALUES = [5, 10, 20, 30, 50]          # 原 [5, 10, 20] — 扩大评估范围
RETRIEVAL_K = 50                          # 各策略统一检索 50 个（原 20）
RRF_K_VALUES = [10, 20, 30, 60]          # RRF-K 消融实验值

# 评估用候选池参数（不影响生产配置）
EVAL_VECTOR_K = chroma_conf.get("eval_vector_k", 50)
EVAL_BM25_K = chroma_conf.get("eval_bm25_k", 50)
EVAL_RRF_OUTPUT_K = chroma_conf.get("eval_rrf_output_k", 50)
EVAL_RERANK_INPUT_K = chroma_conf.get("eval_rerank_input_k", 50)
EVAL_RERANK_OUTPUT_K = chroma_conf.get("eval_rerank_output_k", 8)
# 大候选池消融：放大 Reranker 输入/输出
EVAL_BM25_LARGE_K = 200
EVAL_RERANK_LARGE_INPUT_K = 200
EVAL_RERANK_LARGE_OUTPUT_K = 20


def load_test_questions(path: str) -> list[dict]:
    questions = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                questions.append(json.loads(line))
    return questions


def load_chunk_meta_map() -> dict[str, dict]:
    """从 ChromaDB 加载 chunk_id → metadata 映射（用于 window chunk recall）"""
    client = chromadb.PersistentClient(path=get_abs_path("chroma_db"))
    collection = client.get_collection(chroma_conf["collection_name"])
    all_data = collection.get(include=["metadatas"], limit=5000)
    meta_map = {}
    for m in all_data["metadatas"]:
        cid = m.get("chunk_id", "")
        if cid:
            meta_map[cid] = m
    return meta_map


# ---------- 匹配 ----------

def doc_matches_source(doc: Document, filename_contains: str) -> bool:
    """文档是否来自期望论文：source_file > paper_id > paper_title"""
    fn = filename_contains.lower()
    if fn in doc.metadata.get("source_file", "").lower():
        return True
    if fn in doc.metadata.get("paper_id", "").lower():
        return True
    if fn in doc.metadata.get("paper_title", "").lower():
        return True
    return False


def doc_matches_source_and_page(doc: Document, filename_contains: str, pages: list[int]) -> bool:
    """文档是否来自期望论文 且 页码范围与期望页有交集"""
    if not doc_matches_source(doc, filename_contains):
        return False
    ps = doc.metadata.get("page_start")
    pe = doc.metadata.get("page_end")
    if ps is None:
        ps = pe = doc.metadata.get("page")
    if ps is None:
        return False
    for p in pages:
        if int(ps) <= p <= int(pe):
            return True
    return False


# ---------- 指标 ----------

def compute_source_recall_at_k(
    retrieved: list[Document], expected_sources: list[dict], k: int
) -> float:
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
    return len(hit) / len(expected_sources) if expected_sources else None


def compute_evidence_recall_at_k(
    retrieved: list[Document], expected_sources: list[dict], k: int
) -> float:
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


def compute_source_hit_at_k(
    retrieved: list[Document], expected_sources: list[dict], k: int
) -> float:
    if not expected_sources:
        return None
    for doc in retrieved[:k]:
        for es in expected_sources:
            fn = es.get("filename_contains", "")
            if fn and doc_matches_source(doc, fn):
                return 1.0
    return 0.0


def compute_all_sources_hit_at_k(
    retrieved: list[Document], expected_sources: list[dict], k: int
) -> float:
    if not expected_sources:
        return None
    top_k = retrieved[:k]
    for es in expected_sources:
        fn = es.get("filename_contains", "")
        if not fn:
            continue
        if not any(doc_matches_source(doc, fn) for doc in top_k):
            return 0.0
    return 1.0


def compute_source_mrr(
    retrieved: list[Document], expected_sources: list[dict]
) -> float:
    if not expected_sources:
        return None
    for rank, doc in enumerate(retrieved, 1):
        for es in expected_sources:
            fn = es.get("filename_contains", "")
            if fn and doc_matches_source(doc, fn):
                return 1.0 / rank
    return 0.0


def compute_keyword_coverage_at_k(
    retrieved: list[Document], must_contain: list, k: int
) -> float:
    if not must_contain:
        return None
    top_k_text = " ".join(d.page_content for d in retrieved[:k]).lower()
    hits = 0
    for item in must_contain:
        if isinstance(item, str):
            if item.lower() in top_k_text:
                hits += 1
        elif isinstance(item, list):
            if any(alias.lower() in top_k_text for alias in item):
                hits += 1
    return hits / len(must_contain)


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


def compute_strict_chunk_recall_at_k(
    retrieved: list[Document], expected_chunk_ids: list[str], k: int
) -> float | None:
    """Strict Chunk Recall@k：group 内任一 cid 命中即算该 group 命中"""
    groups = _normalize_chunk_groups(expected_chunk_ids)
    if not groups:
        return None
    retrieved_ids = set(d.metadata.get("chunk_id", "") for d in retrieved[:k])
    hits = sum(1 for group in groups if any(cid in retrieved_ids for cid in group))
    return hits / len(groups)


def compute_window_chunk_recall_at_k(
    retrieved: list[Document], expected_chunk_ids: list[str], k: int,
    chunk_meta_map: dict,
) -> float | None:
    """Window Chunk Recall@k：group 内任一 cid 命中即算该 group 命中（含精确+窗口容错）"""
    groups = _normalize_chunk_groups(expected_chunk_ids)
    if not groups:
        return None
    retrieved_slice = retrieved[:k]
    hits = 0
    for group in groups:
        # 精确命中：group 内任一 cid
        if any(d.metadata.get("chunk_id", "") in group for d in retrieved_slice):
            hits += 1
            continue
        # 窗口容错：对 group 内每个 cid 尝试
        window_hit = False
        for cid in group:
            exp_meta = chunk_meta_map.get(cid)
            if not exp_meta:
                continue
            exp_pid = exp_meta.get("paper_id", "")
            exp_sec = exp_meta.get("section", "")
            exp_idx = exp_meta.get("chunk_index", -1)
            exp_ps = exp_meta.get("page_start", 0)
            for d in retrieved_slice:
                if (d.metadata.get("paper_id") == exp_pid
                    and d.metadata.get("section") == exp_sec
                    and abs(d.metadata.get("chunk_index", -1) - exp_idx) <= 1
                    and abs(d.metadata.get("page_start", 0) - exp_ps) <= 1):
                    window_hit = True
                    break
            if window_hit:
                break
        if window_hit:
            hits += 1
    return hits / len(groups)


# ---------- 辅助：按 chunk_meta_map 计算 chunk_recall（通用） ----------

def _chunk_recall_for_docs(
    docs: list[Document], expected_chunk_ids: list[str], k: int,
    chunk_meta_map: dict,
) -> tuple[float | None, float | None]:
    """返回 (strict_recall, window_recall)"""
    if not expected_chunk_ids:
        return None, None
    strict = compute_strict_chunk_recall_at_k(docs, expected_chunk_ids, k)
    window = compute_window_chunk_recall_at_k(docs, expected_chunk_ids, k, chunk_meta_map)
    return strict, window


# ---------- MQ RRF 检索 ----------

def _mq_rrf_retrieve(query: str, mq_plan: dict, bm25, vs, hyb_scorer, top_k=50):
    """MQ RRF Fusion：MQ pool → per-subquery HybridScorer 打分 → RRF(k=60) 融合 → BM25 保底"""
    subqueries = mq_plan.get("subqueries", [{"entity": "fallback", "query": query}])
    if not subqueries:
        subqueries = [{"entity": "fallback", "query": query}]

    mq_pool = multi_query_retrieve(subqueries, bm25, vs, hyb_scorer)
    if not mq_pool:
        return hyb_scorer.retrieve(query, bm25_k=50, top_k=top_k)

    all_subq_scores = []
    all_subq_bm25 = []
    for sq in subqueries:
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

    # RRF fusion
    RRF_K = 60
    rrf_scores: dict[int, float] = {}
    for sq_scores in all_subq_scores:
        ranked = sorted(sq_scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (i, _) in enumerate(ranked, 1):
            rrf_scores[i] = rrf_scores.get(i, 0) + 1.0 / (RRF_K + rank)

    # BM25 safeguard
    N = len(mq_pool)
    bm25_max = {i: max(bs[i] for bs in all_subq_bm25) for i in range(N)}

    ranking = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
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


# ---------- 主流程 ----------

def run_eval():
    all_questions = load_test_questions(CHUNK_EVAL_PATH)
    os.makedirs(REPORT_DIR, exist_ok=True)

    answerable = [q for q in all_questions if q.get("should_answer", True)
                  and q.get("id") not in ("", "")]

                  # and q.get("id") not in ("cross_002_en", "cross_002_zh")]
    unanswerable = [q for q in all_questions if not q.get("should_answer", True)]

    print(f"加载 {len(all_questions)} 题：可答 {len(answerable)}（已排除cross_002），不可答 {len(unanswerable)}")

    # 加载 chunk 元数据映射
    chunk_meta_map = load_chunk_meta_map()
    print(f"Chunk 元数据映射：{len(chunk_meta_map)} 条")

    # 初始化组件
    vs = VectorStoreService()
    bm25 = BM25Store()
    bm25.load()
    bm25.add_domain_terms()

    hybrid = HybridRetriever(
        vector_store=vs.vector_store,
        bm25_store=bm25,
        rrf_fusion_k_override=EVAL_RRF_OUTPUT_K,
    )
    reranker_baseline = Reranker()                                                      # 基线：无 passage 无 fusion
    reranker_enhanced = Reranker(passage_mode=True)                                     # 增强 passage，无 fusion
    reranker_fusion_07 = Reranker(passage_mode=True, fusion_enabled=True, alpha=0.7)    # fusion alpha=0.7
    reranker_fusion_08 = Reranker(passage_mode=True, fusion_enabled=True, alpha=0.8)    # fusion alpha=0.8

    # 生产 RAG 管线：直接使用 RagSummarizeService.retriever_docs()，保证 100% 管线一致性
    rag_service = RagSummarizeService()
    # production_rrf50 变体：RRF 候选池扩大到 50（其余参数与生产完全一致）
    hybrid_rrf50 = HybridRetriever(
        vector_store=vs.vector_store,
        bm25_store=bm25,
        rrf_fusion_k_override=50,
    )

    # ─── 大候选池消融：BM25→Rerank（跳过 RRF 向量噪声）───
    bm25_large_retriever = BM25Store()
    bm25_large_retriever.load()
    bm25_large_retriever.add_domain_terms()
    reranker_bm25_large = Reranker(passage_mode=True, fusion_enabled=False)               # BM25 only, no vector fusion
    reranker_hybrid_large = Reranker(passage_mode=True, fusion_enabled=True, alpha=0.7)   # RRF + large pool

    # ─── 混合保底打分：BM25 + Reranker + Keyword + Metadata（Reranker 不作为硬截断器）───
    hybrid_scorer = HybridScorer(bm25_store=bm25, reranker=Reranker(passage_mode=True, fusion_enabled=False))

    # ─── 预计算 MQ RRF Fusion 结果 ───
    with open(MULTI_CACHE_PATH) as f:
        multi_cache = json.load(f)

    # ─── 加载中→英翻译缓存 + 预检测全部题目 ───
    zh_cache = _load_zh_translate_cache()
    tr_count = 0
    for q in all_questions:
        result = _translate_zh_query(q["question"], zh_cache)
        if result != q["question"]:
            tr_count += 1
    print(f"语言检测+翻译：{tr_count} 题需要翻译（共 {len(all_questions)} 题）")

    mq_rrf_results: dict[str, list[Document]] = {}
    for q in all_questions:
        query = q["question"]
        qid = q["id"]
        mq_plan = multi_cache.get(qid, {"subqueries": [{"entity": "fallback", "query": query}]})
        try:
            mq_rrf_results[query] = _mq_rrf_retrieve(query, mq_plan, bm25, vs, hybrid_scorer)
        except Exception as e:
            logger.warning(f"[MQ RRF] {qid} 预计算失败：{e}")
            mq_rrf_results[query] = hybrid_scorer.retrieve(query, bm25_k=50, top_k=50)

    # ─── 十四大策略 ───
    strategies = {
        "vector_only": lambda q: vs.vector_store.as_retriever(
            search_kwargs={"k": RETRIEVAL_K}
        ).invoke(q),
        "hybrid_no_rerank": lambda q: hybrid.retrieve(q, k=RETRIEVAL_K),
        "hybrid_rerank": lambda q: reranker_baseline.rerank(
            q, hybrid.retrieve(q, k=EVAL_RERANK_INPUT_K), top_k=EVAL_RERANK_OUTPUT_K
        ),
        "hybrid_rerank_translate": lambda q: reranker_baseline.rerank(
            _translate_zh_query(q, zh_cache),
            hybrid.retrieve(_translate_zh_query(q, zh_cache), k=EVAL_RERANK_INPUT_K),
            top_k=EVAL_RERANK_OUTPUT_K,
        ),
        "hybrid_rerank_enhanced": lambda q: reranker_enhanced.rerank(
            q, hybrid.retrieve(q, k=EVAL_RERANK_INPUT_K), top_k=EVAL_RERANK_OUTPUT_K
        ),
        "hybrid_rerank_fusion_07": lambda q: reranker_fusion_07.rerank(
            q, hybrid.retrieve(q, k=EVAL_RERANK_INPUT_K), top_k=EVAL_RERANK_OUTPUT_K
        ),
        "hybrid_rerank_fusion_08": lambda q: reranker_fusion_08.rerank(
            q, hybrid.retrieve(q, k=EVAL_RERANK_INPUT_K), top_k=EVAL_RERANK_OUTPUT_K
        ),
        # 大候选池消融
        "bm25_rerank_large": lambda q: reranker_bm25_large.rerank(
            q, [d for d, _ in bm25_large_retriever.search(q, EVAL_BM25_LARGE_K)],
            top_k=EVAL_RERANK_LARGE_OUTPUT_K,
        ),
        "hybrid_rerank_large": lambda q: reranker_hybrid_large.rerank(
            q, hybrid.retrieve(q, k=EVAL_RERANK_LARGE_INPUT_K),
            top_k=EVAL_RERANK_LARGE_OUTPUT_K,
        ),
        # 混合保底打分（BM25+Rerank+Keyword+Meta，不硬截断）
        "hybrid_score": lambda q: hybrid_scorer.retrieve(q, bm25_k=50, top_k=20),
        # Raw Query：同管线 top_k=50（对齐 RETRIEVAL_K）
        "hybrid_score_raw": lambda q: hybrid_scorer.retrieve(q, bm25_k=50, top_k=50),
        # 翻译 + HybridScorer：与 multi_query_eval 的 tr 对齐，2×2 消融用
        "hybrid_score_translate": lambda q: hybrid_scorer.retrieve(
            _translate_zh_query(q, zh_cache), bm25_k=50, top_k=50
        ),
        # MQ RRF Fusion：多查询结构化检索 + RRF 排名融合
        "mq_rrf": lambda q: mq_rrf_results.get(q, []),
        # 生产管线：直接调用 RagSummarizeService.retriever_docs()，与 Agent 实际检索路径 100% 一致
        "production": lambda q: rag_service.retriever_docs(q),
        # 生产管线变体：RRF 候选池从 20 扩大到 50（其余管线完全一致）
        "production_rrf50": lambda q: rag_service.reranker.rerank(
            rag_service._rewrite_query(q),
            hybrid_rrf50.retrieve(rag_service._rewrite_query(q)),
        ),
        # 生产管线变体：用 LLM 中文翻译英文 替代 规则缩写展开（跳过 _rewrite_query，其余管线完全一致）
        "production_translate": lambda q: (lambda tq: rag_service.reranker.rerank(
            tq, rag_service.hybrid_retriever.retrieve(tq)
        ))(_translate_zh_query(q, zh_cache)),
    }

    # 累积桶
    result_answerable: dict[str, dict[str, list[float]]] = {
        name: defaultdict(list) for name in strategies
    }
    result_unanswerable: dict[str, dict[str, list[float]]] = {
        name: defaultdict(list) for name in strategies
    }

    # ─── 分阶段召回累积 ───
    staged_answerable: dict[str, dict[str, list[float]]] = {
        "vector_30": defaultdict(list), "vector_50": defaultdict(list),
        "bm25_30": defaultdict(list), "bm25_50": defaultdict(list),
        "union_60": defaultdict(list),
        "rrf_20": defaultdict(list), "rrf_50": defaultdict(list),
        "rerank_5": defaultdict(list), "rerank_10": defaultdict(list),
        "bm25_200": defaultdict(list),
        "rerank_large_10": defaultdict(list), "rerank_large_20": defaultdict(list),
    }

    # ─── 边界指标 + 分类统计 ───
    boundary_data: dict[str, list[dict]] = {"unanswerable": [], "answerable": []}
    category_stats: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    # 类别从 answer_type 字段动态推导（fallback: 从 id 前缀推断）
    id_to_category = {}
    for q in all_questions:
        qid = q["id"]
        cat = q.get("answer_type", qid.split("_")[0] if "_" in qid else "other")
        id_to_category[qid] = cat

    vector_retriever_30 = vs.vector_store.as_retriever(search_kwargs={"k": 30})
    vector_retriever_50 = vs.vector_store.as_retriever(search_kwargs={"k": 50})

    for qset, result_bucket, label in [
        (answerable, result_answerable, "answerable"),
        (unanswerable, result_unanswerable, "unanswerable"),
    ]:
        for i, q in enumerate(qset, 1):
            query = q["question"]
            expected = q.get("expected_sources", [])
            must_contain = q.get("must_contain", [])
            expected_chunk_ids = q.get("expected_chunk_ids", [])

            print(f"[{label} {i}/{len(qset)}] {query[:70]}...")

            # ── 分阶段召回（仅对可答题） ──
            if label == "answerable" and expected_chunk_ids:
                try:
                    vec30 = vector_retriever_30.invoke(query)
                    sr30, wr30 = _chunk_recall_for_docs(vec30, expected_chunk_ids, 30, chunk_meta_map)
                    if sr30 is not None: staged_answerable["vector_30"]["strict"].append(sr30)
                    if wr30 is not None: staged_answerable["vector_30"]["window"].append(wr30)
                except Exception:
                    pass
                try:
                    vec50 = vector_retriever_50.invoke(query)
                    sr50, wr50 = _chunk_recall_for_docs(vec50, expected_chunk_ids, 50, chunk_meta_map)
                    if sr50 is not None: staged_answerable["vector_50"]["strict"].append(sr50)
                    if wr50 is not None: staged_answerable["vector_50"]["window"].append(wr50)
                except Exception:
                    pass
                try:
                    bm25_30 = [d for d, _ in bm25.search(query, 30)]
                    sr, wr = _chunk_recall_for_docs(bm25_30, expected_chunk_ids, 30, chunk_meta_map)
                    if sr is not None: staged_answerable["bm25_30"]["strict"].append(sr)
                    if wr is not None: staged_answerable["bm25_30"]["window"].append(wr)
                except Exception:
                    pass
                try:
                    bm25_50 = [d for d, _ in bm25.search(query, 50)]
                    sr, wr = _chunk_recall_for_docs(bm25_50, expected_chunk_ids, 50, chunk_meta_map)
                    if sr is not None: staged_answerable["bm25_50"]["strict"].append(sr)
                    if wr is not None: staged_answerable["bm25_50"]["window"].append(wr)
                except Exception:
                    pass
                try:
                    # Union: 向量 + BM25（按 page_content MD5 去重）
                    union_docs = []
                    seen = set()
                    for d in vec50 + bm25_50:
                        key = d.page_content[:120]
                        if key not in seen:
                            seen.add(key)
                            union_docs.append(d)
                    sr, wr = _chunk_recall_for_docs(union_docs, expected_chunk_ids, 60, chunk_meta_map)
                    if sr is not None: staged_answerable["union_60"]["strict"].append(sr)
                    if wr is not None: staged_answerable["union_60"]["window"].append(wr)
                except Exception:
                    pass

            # ── 主策略评估 ──
            for name, fn in strategies.items():
                try:
                    retrieved = fn(query)
                except Exception as e:
                    logger.warning(f"[Eval]{name} 检索失败：{e}")
                    retrieved = []

                for k in K_VALUES:
                    sr = compute_source_recall_at_k(retrieved, expected, k)
                    er = compute_evidence_recall_at_k(retrieved, expected, k)
                    sh = compute_source_hit_at_k(retrieved, expected, k)
                    ah = compute_all_sources_hit_at_k(retrieved, expected, k)
                    kc = compute_keyword_coverage_at_k(retrieved, must_contain, k)
                    scr = compute_strict_chunk_recall_at_k(retrieved, expected_chunk_ids, k)
                    wcr = compute_window_chunk_recall_at_k(retrieved, expected_chunk_ids, k, chunk_meta_map)

                    for val, key in [
                        (sr, f"source_recall@{k}"),
                        (er, f"evidence_recall@{k}"),
                        (sh, f"source_hit@{k}"),
                        (ah, f"all_sources_hit@{k}"),
                        (kc, f"keyword_coverage@{k}"),
                        (scr, f"strict_chunk_recall@{k}"),
                        (wcr, f"window_chunk_recall@{k}"),
                    ]:
                        if val is not None:
                            result_bucket[name][key].append(val)

                mrr = compute_source_mrr(retrieved, expected)
                if mrr is not None:
                    result_bucket[name]["source_mrr"].append(mrr)

                # 收集 boundary 数据 + 分类统计（fusion_07 策略）
                if name == "hybrid_rerank_fusion_07":
                    max_rs = max(reranker_fusion_07.last_reranker_scores) if reranker_fusion_07.last_reranker_scores else 0
                    max_fs = max(reranker_fusion_07.last_fusion_scores) if reranker_fusion_07.last_fusion_scores else 0
                    if label == "answerable":
                        # 分类统计（k=20 已在上面计算，直接复用 scr/wcr）
                        cat = id_to_category.get(q["id"], "其他")
                        scr20 = compute_strict_chunk_recall_at_k(retrieved, expected_chunk_ids, 20)
                        wcr20 = compute_window_chunk_recall_at_k(retrieved, expected_chunk_ids, 20, chunk_meta_map)
                        sr20 = compute_source_recall_at_k(retrieved, expected, 20)
                        er20 = compute_evidence_recall_at_k(retrieved, expected, 20)
                        mrr = compute_source_mrr(retrieved, expected)
                        if scr20 is not None: category_stats[cat]["strict_chunk_recall@20"].append(scr20)
                        if wcr20 is not None: category_stats[cat]["window_chunk_recall@20"].append(wcr20)
                        if sr20 is not None: category_stats[cat]["source_recall@20"].append(sr20)
                        if er20 is not None: category_stats[cat]["evidence_recall@20"].append(er20)
                        if mrr is not None: category_stats[cat]["source_mrr"].append(mrr)
                        boundary_data["answerable"].append({
                            "id": q["id"], "max_reranker_score": max_rs, "max_fusion_score": max_fs,
                        })
                    elif label == "unanswerable":
                        boundary_data["unanswerable"].append({
                            "id": q["id"], "question": q["question"][:60],
                            "max_reranker_score": max_rs, "max_fusion_score": max_fs,
                            "evidence_triggered": max_fs > 0.3,
                        })

                # 分阶段：记录 RRF + Rerank（用 fusion 0.7 版本）的 chunk recall
                if label == "answerable" and expected_chunk_ids and name == "hybrid_rerank_fusion_07":
                    try:
                        rrf_docs = hybrid.retrieve(query, k=EVAL_RRF_OUTPUT_K)
                        sr, wr = _chunk_recall_for_docs(rrf_docs, expected_chunk_ids, 50, chunk_meta_map)
                        if sr is not None: staged_answerable["rrf_50"]["strict"].append(sr)
                        if wr is not None: staged_answerable["rrf_50"]["window"].append(wr)

                        rrf_20 = rrf_docs[:20]
                        sr2, wr2 = _chunk_recall_for_docs(rrf_20, expected_chunk_ids, 20, chunk_meta_map)
                        if sr2 is not None: staged_answerable["rrf_20"]["strict"].append(sr2)
                        if wr2 is not None: staged_answerable["rrf_20"]["window"].append(wr2)

                        rerank_docs = reranker_fusion_07.rerank(query, rrf_docs, top_k=5)
                        sr3, wr3 = _chunk_recall_for_docs(rerank_docs, expected_chunk_ids, 5, chunk_meta_map)
                        if sr3 is not None: staged_answerable["rerank_5"]["strict"].append(sr3)
                        if wr3 is not None: staged_answerable["rerank_5"]["window"].append(wr3)

                        rerank_10 = reranker_fusion_07.rerank(query, rrf_docs, top_k=10)
                        sr4, wr4 = _chunk_recall_for_docs(rerank_10, expected_chunk_ids, 10, chunk_meta_map)
                        if sr4 is not None: staged_answerable["rerank_10"]["strict"].append(sr4)
                        if wr4 is not None: staged_answerable["rerank_10"]["window"].append(wr4)
                    except Exception:
                        pass

                # ── 大候选池消融阶段（仅对可答题）──
                if label == "answerable" and expected_chunk_ids:
                    try:
                        bm25_200_docs = [d for d, _ in bm25_large_retriever.search(query, EVAL_BM25_LARGE_K)]
                        sr, wr = _chunk_recall_for_docs(bm25_200_docs, expected_chunk_ids, 200, chunk_meta_map)
                        if sr is not None: staged_answerable["bm25_200"]["strict"].append(sr)
                        if wr is not None: staged_answerable["bm25_200"]["window"].append(wr)
                    except Exception:
                        pass
                    try:
                        rrf_large_docs = hybrid.retrieve(query, k=EVAL_RERANK_LARGE_INPUT_K)
                        rl_10 = reranker_hybrid_large.rerank(query, rrf_large_docs, top_k=10)
                        sr, wr = _chunk_recall_for_docs(rl_10, expected_chunk_ids, 10, chunk_meta_map)
                        if sr is not None: staged_answerable["rerank_large_10"]["strict"].append(sr)
                        if wr is not None: staged_answerable["rerank_large_10"]["window"].append(wr)

                        rl_20 = reranker_hybrid_large.rerank(query, rrf_large_docs, top_k=EVAL_RERANK_LARGE_OUTPUT_K)
                        sr2, wr2 = _chunk_recall_for_docs(rl_20, expected_chunk_ids, EVAL_RERANK_LARGE_OUTPUT_K, chunk_meta_map)
                        if sr2 is not None: staged_answerable["rerank_large_20"]["strict"].append(sr2)
                        if wr2 is not None: staged_answerable["rerank_large_20"]["window"].append(wr2)
                    except Exception:
                        pass

    # ────────── 报告 ──────────

    report = []
    report.append("# 检索策略消融评估报告 v3")
    report.append("")
    report.append(f"评估时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"可答题：{len(answerable)} | 不可答题：{len(unanswerable)} | 全库 chunk：{len(chunk_meta_map)}")
    report.append(f"K_VALUES：{K_VALUES} | RETRIEVAL_K：{RETRIEVAL_K}")
    report.append(f"Reranker 输出：top-{EVAL_RERANK_OUTPUT_K} | 候选池：{EVAL_RERANK_INPUT_K}")
    report.append(f"大池消融：BM25@{EVAL_BM25_LARGE_K} → Rerank(no-fusion)@{EVAL_RERANK_LARGE_OUTPUT_K} | RRF@{EVAL_RERANK_LARGE_INPUT_K} → Rerank(fusion)@{EVAL_RERANK_LARGE_OUTPUT_K}")
    report.append(f"混合打分：BM25(45%)+Rerank(25%)+Keyword(20%)+Meta(10%)，BM25 top-5 保底 | 不硬截断")
    report.append(f"Fusion alpha：0.7/0.8 | passage_mode：基线/增强/fusion")
    report.append("")

    # === 分阶段召回 ===
    _write_staged_recall_table(report, staged_answerable)

    # === Chunk ID 诊断 ===
    _write_chunks_diag(report, all_questions, chunk_meta_map)

    # === 可答题指标 ===
    _write_metric_table(report, "## 可答题检索指标（十四大策略）", result_answerable, strategies)

    # === 分类统计 ===
    _write_category_stats(report, category_stats)

    # === 边界指标 ===
    _write_boundary_metrics(report, boundary_data)

    # === 不可答题指标 ===
    report.append("")
    report.append("## 不可答题（知识边界）")
    report.append("")
    report.append("不可答题 `should_answer=false`，期望检索不到相关内容。以下指标越低越好：")
    report.append("")
    _write_metric_table(report, "### 不可答题检索指标", result_unanswerable, strategies)

    # === RRF-K 消融 ===
    report.append("")
    report.append("---")
    report.append("")
    report.append("## RRF-K 消融实验")
    report.append("")
    report.append(f"固定参数：hybrid_k={RETRIEVAL_K} rerank_top_k={EVAL_RERANK_OUTPUT_K}")
    report.append("")
    _run_rrf_k_ablation(report, answerable, vs, bm25, chunk_meta_map)

    # 逐题详情
    report.append("")
    report.append("---")
    report.append("")
    report.append("## 逐题详情（可答题）")
    report.append("")
    for q in answerable:
        expected_fns = [es.get("filename_contains", "") for es in q.get("expected_sources", [])]
        report.append(f"- **{q['id']}** [{q.get('answer_type', '')}] {q['question'][:80]}")
        report.append(f"  期望来源: {expected_fns} | pages: {[es.get('pages_any', []) for es in q.get('expected_sources', [])]} | chunks: {len(q.get('expected_chunk_ids', []))}")
    report.append("")

    full_report = "\n".join(report)
    print("\n" + full_report)

    ts = datetime.now().strftime("%Y%m%d_%H%M")
    report_path = os.path.join(REPORT_DIR, f"retrieval_ablation_{ts}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(full_report)
    print(f"报告已保存至：{report_path}")

    return full_report


def _write_category_stats(
    report: list[str],
    category_stats: dict[str, dict[str, list[float]]],
):
    """按类别分组统计 strict/window chunk_recall + source/evidence recall + source_mrr @20"""
    report.append("## 按题型分类统计（hybrid_rerank_fusion_07 @20）")
    report.append("")
    header = "| 类别 | 题数 | source_recall | evidence_recall | source_mrr | strict_chunk_recall | window_chunk_recall |"
    sep = "|------|------|-------------|---------------|-----------|-------------------|-------------------|"
    report.append(header)
    report.append(sep)

    ordered_cats = sorted(category_stats.keys())
    for cat in ordered_cats:
        if cat not in category_stats:
            continue
        stats = category_stats[cat]
        src_vals = stats.get("source_recall@20", [])
        evd_vals = stats.get("evidence_recall@20", [])
        mrr_vals = stats.get("source_mrr", [])
        strict_vals = stats.get("strict_chunk_recall@20", [])
        window_vals = stats.get("window_chunk_recall@20", [])
        n = len(strict_vals)
        if n == 0:
            continue
        avg_src = sum(src_vals) / len(src_vals) if src_vals else 0.0
        avg_evd = sum(evd_vals) / len(evd_vals) if evd_vals else 0.0
        avg_mrr = sum(mrr_vals) / len(mrr_vals) if mrr_vals else 0.0
        avg_s = sum(strict_vals) / n
        avg_w = sum(window_vals) / n
        report.append(f"| {cat} | {n} | {avg_src:.3f} | {avg_evd:.3f} | {avg_mrr:.3f} | {avg_s:.3f} | {avg_w:.3f} |")
    report.append("")


def _write_boundary_metrics(
    report: list[str],
    boundary_data: dict[str, list[dict]],
):
    """边界指标：answerability_accuracy / abstention / unsupported evidence"""
    report.append("## 边界指标（知识边界与证据质量）")
    report.append("")

    # ── Answerability Accuracy（检索级） ──
    # 不可答题：max_fusion_score < 0.3 → 正确拒答
    # 可答题：max_fusion_score >= 0.3 → 正确触发
    THRESHOLD = 0.3
    unans = boundary_data.get("unanswerable", [])
    ans = boundary_data.get("answerable", [])

    unans_correct = sum(1 for item in unans if item["max_fusion_score"] < THRESHOLD)
    ans_correct = sum(1 for item in ans if item["max_fusion_score"] >= THRESHOLD)
    total_correct = unans_correct + ans_correct
    total_all = len(unans) + len(ans)
    answerability_acc = total_correct / total_all if total_all > 0 else 0.0
    abstention_rate = unans_correct / len(unans) if unans else 1.0
    false_answer_rate = sum(1 for item in unans if item["max_fusion_score"] >= THRESHOLD) / len(unans) if unans else 0.0

    report.append("### Answerability Accuracy（检索级可答性判断）")
    report.append("")
    report.append(f"- **Answerability Accuracy**: {answerability_acc:.2%} "
                   f"（{total_correct}/{total_all}，阈值 fusion_score={THRESHOLD}）")
    report.append(f"- **Abstention Rate（正确拒答率）**: {abstention_rate:.2%} "
                   f"（{unans_correct}/{len(unans)} 不可答题 max_fusion < {THRESHOLD}）")
    report.append(f"- **False Answer Rate（误答率）**: {false_answer_rate:.2%} "
                   f"（{len(unans) - unans_correct}/{len(unans)} 不可答题被触发）")
    report.append(f"- **Correct Trigger Rate（可答题正确触发率）**: {ans_correct / len(ans):.2%} "
                   f"（{ans_correct}/{len(ans)} 可答题 max_fusion >= {THRESHOLD}）")
    report.append("")

    # ── 不可答题详情 ──
    if unans:
        report.append("### 不可答题 — Reranker 触发风险")
        report.append("")
        header = "| ID | Question | Max Reranker Score | Max Fusion Score | 误触发 |"
        sep = "|------|----------|-------------------|-----------------|--------|"
        report.append(header)
        report.append(sep)
        for item in unans:
            trig = "⚠ 是" if item["max_fusion_score"] >= THRESHOLD else "否"
            report.append(
                f"| {item['id']} | {item['question']} | {item['max_reranker_score']:.3f} | "
                f"{item['max_fusion_score']:.3f} | {trig} |"
            )
        report.append("")

    # ── 可答题证据充分性 ──
    if ans:
        report.append("### 可答题 — 证据充分性")
        report.append("")
        low_evidence = [item for item in ans if item["max_fusion_score"] < THRESHOLD]
        unsupported_rate = len(low_evidence) / len(ans) if ans else 0.0
        avg_max_rs = sum(item["max_reranker_score"] for item in ans) / len(ans)
        avg_max_fs = sum(item["max_fusion_score"] for item in ans) / len(ans)
        report.append(f"- **Avg Max Reranker Score**: {avg_max_rs:.3f}")
        report.append(f"- **Avg Max Fusion Score**: {avg_max_fs:.3f}")
        report.append(f"- **Unsupported Evidence Rate（证据不足率）**: {unsupported_rate:.2%} "
                       f"（{len(low_evidence)}/{len(ans)} 题 max_fusion_score < {THRESHOLD}）")
        if low_evidence:
            report.append(f"- 低证据题：{', '.join(item['id'] for item in low_evidence)}")
        report.append("")


def _run_rrf_k_ablation(
    report: list[str],
    answerable: list[dict],
    vs, bm25, chunk_meta_map,
):
    """RRF-K 消融：测试不同 rrf_k 值下的 chunk_recall"""
    header = "| rrf_k | strict_chunk_recall@20 | window_chunk_recall@20 |"
    sep = "|------|----------------------|----------------------|"
    report.append(header)
    report.append(sep)

    for rrf_k in RRF_K_VALUES:
        hybrid_test = HybridRetriever(
            vector_store=vs.vector_store,
            bm25_store=bm25,
            rrf_k_override=rrf_k,
            hybrid_k_override=RETRIEVAL_K,
            rrf_fusion_k_override=EVAL_RRF_OUTPUT_K,
        )
        strict_vals = []
        window_vals = []
        for q in answerable:
            expected_chunk_ids = q.get("expected_chunk_ids", [])
            if not expected_chunk_ids:
                continue
            try:
                docs = hybrid_test.retrieve(q["question"], k=EVAL_RRF_OUTPUT_K)
                s = compute_strict_chunk_recall_at_k(docs, expected_chunk_ids, 20)
                w = compute_window_chunk_recall_at_k(docs, expected_chunk_ids, 20, chunk_meta_map)
                if s is not None: strict_vals.append(s)
                if w is not None: window_vals.append(w)
            except Exception as e:
                logger.warning(f"[RRF-K消融] rrf_k={rrf_k} {q['id']} 失败：{e}")
        avg_s = sum(strict_vals) / len(strict_vals) if strict_vals else 0.0
        avg_w = sum(window_vals) / len(window_vals) if window_vals else 0.0
        marker = " ← 当前" if rrf_k == chroma_conf.get("rrf_k", 60) else ""
        report.append(f"| {rrf_k} | {avg_s:.3f} | {avg_w:.3f} |{marker}")


def _write_staged_recall_table(
    report: list[str],
    staged: dict[str, dict[str, list[float]]],
):
    """输出分阶段召回统计表"""
    report.append("## 分阶段召回统计（strict / window chunk_recall）")
    report.append("")
    header = "| 阶段 | strict_chunk_recall | window_chunk_recall | 说明 |"
    sep = "|------|-------------------|-------------------|------|"
    report.append(header)
    report.append(sep)

    stages = [
        ("vector_30", "Vector @30", "向量检索 top-30"),
        ("vector_50", "Vector @50", "向量检索 top-50"),
        ("bm25_30", "BM25 @30", "BM25 关键词 top-30"),
        ("bm25_50", "BM25 @50", "BM25 关键词 top-50"),
        ("bm25_200", "BM25 @200", "BM25 关键词 top-200"),
        ("union_60", "Union @60", "向量+BM25 去重合并 top-60"),
        ("rrf_20", "RRF @20", "RRF 融合后 top-20"),
        ("rrf_50", "RRF @50", "RRF 融合后 top-50"),
        ("rerank_5", "Rerank @5", "Reranker 精排 top-5"),
        ("rerank_10", "Rerank @10", "Reranker 精排 top-10"),
        ("rerank_large_10", "Rerank-large @10", "RRF@200→Rerank(fusion) top-10"),
        ("rerank_large_20", "Rerank-large @20", "RRF@200→Rerank(fusion) top-20"),
    ]

    for key, label, desc in stages:
        strict_vals = staged.get(key, {}).get("strict", [])
        window_vals = staged.get(key, {}).get("window", [])
        avg_strict = sum(strict_vals) / len(strict_vals) if strict_vals else 0.0
        avg_window = sum(window_vals) / len(window_vals) if window_vals else 0.0
        report.append(f"| {label} | {avg_strict:.3f} | {avg_window:.3f} | {desc} |")
    report.append("")


def _write_chunks_diag(
    report: list[str],
    all_questions: list[dict],
    chunk_meta_map: dict[str, dict],
):
    """诊断报告：chunks=0 的题目 + stale chunk_id 检测"""
    report.append("## Chunk ID 诊断")
    report.append("")

    # 可答题中 expected_chunk_ids 为空的
    empty_chunks = [q for q in all_questions
                    if q.get("should_answer", True) and not q.get("expected_chunk_ids", [])]
    if empty_chunks:
        report.append("### 可答题但 chunks=0")
        report.append("")
        for q in empty_chunks:
            srcs = [s.get("filename_contains", "") for s in q.get("expected_sources", [])]
            report.append(f"- **{q['id']}**: {q['question'][:80]} | sources={srcs}")
        report.append("")

    # 检测 stale chunk_id（expected 中不存在的 ID）
    all_valid_ids = set(chunk_meta_map.keys())
    stale_report = []
    for q in all_questions:
        expected = q.get("expected_chunk_ids", [])
        if not expected:
            continue
        groups = _normalize_chunk_groups(expected)
        all_cids = [cid for group in groups for cid in group]
        missing = [cid for cid in all_cids if cid not in all_valid_ids]
        if missing:
            stale_report.append((q["id"], missing, len(all_cids)))
    if stale_report:
        report.append("### Stale Chunk ID（expected 中不在当前 ChromaDB 的 ID）")
        report.append("")
        for qid, missing, total in stale_report:
            report.append(f"- **{qid}**: {len(missing)}/{total} stale → `{', '.join(missing[:4])}`"
                          f"{'...' if len(missing) > 4 else ''}")
        report.append("")

    # 统计概览
    answerable_with_chunks = sum(1 for q in all_questions
                                 if q.get("should_answer", True) and q.get("expected_chunk_ids", []))
    report.append(f"- 可答题共 {sum(1 for q in all_questions if q.get('should_answer', True))} 题，"
                   f"其中 {answerable_with_chunks} 题有 chunk_id 标注，"
                   f"{len(empty_chunks)} 题 chunks=0")
    report.append("")


def _write_metric_table(
    report: list[str],
    heading: str,
    result_bucket: dict[str, dict[str, list[float]]],
    strategies: dict,
):
    report.append(heading)
    report.append("")

    strategy_names = list(strategies.keys())
    header = "| 指标 | " + " | ".join(strategy_names) + " |"
    sep = "|------|" + "|".join(["-" * (len(n) + 2) for n in strategy_names]) + "|"
    report.append(header)
    report.append(sep)

    metric_names = []
    for k in K_VALUES:
        metric_names += [f"source_recall@{k}", f"evidence_recall@{k}"]
    metric_names += ["source_mrr"]
    for k in K_VALUES:
        metric_names += [f"source_hit@{k}", f"all_sources_hit@{k}", f"keyword_coverage@{k}"]
    for k in K_VALUES:
        metric_names += [f"strict_chunk_recall@{k}", f"window_chunk_recall@{k}"]

    for metric in metric_names:
        vals = {}
        for name in strategy_names:
            scores = result_bucket[name].get(metric, [])
            vals[name] = sum(scores) / len(scores) if scores else 0.0

        row = "| " + metric + " | " + " | ".join(f"{vals[n]:.3f}" for n in strategy_names) + " |"
        best = max(vals, key=vals.get)
        row += f" 🏆 {best}"
        report.append(row)


if __name__ == "__main__":
    run_eval()

def main(argv=None) -> int:
    """CLI 入口"""
    run_eval()
    return 0
