"""
Multi-Query 检索策略消融评估
基于 multi_query_cache.json，用结构化子查询替换单 query 检索入口，
复现 retrieval_eval.py 的全部 9 个策略 + 分阶段召回 + 分类统计
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from collections import defaultdict, OrderedDict

import chromadb
from langchain_core.documents import Document

from rag.vector_store import VectorStoreService
from rag.bm25_store import BM25Store
from rag.retrieval_strategy import HybridRetriever, Reranker, HybridScorer
from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

# ─── 配置 ───
EVAL_PATH = get_abs_path("evaluation/rag_eval_20.jsonl")
MULTI_CACHE_PATH = get_abs_path("evaluation/multi_query_cache.json")
REPORT_DIR = get_abs_path("evaluation/reports")

K_VALUES = [5, 10, 20, 30, 50]
RETRIEVAL_K = 50

EVAL_VECTOR_K = chroma_conf.get("eval_vector_k", 50)
EVAL_BM25_K = chroma_conf.get("eval_bm25_k", 50)
EVAL_RRF_OUTPUT_K = chroma_conf.get("eval_rrf_output_k", 50)
EVAL_RERANK_INPUT_K = chroma_conf.get("eval_rerank_input_k", 50)
EVAL_RERANK_OUTPUT_K = chroma_conf.get("eval_rerank_output_k", 8)
EVAL_BM25_LARGE_K = 200
EVAL_RERANK_LARGE_INPUT_K = 200
EVAL_RERANK_LARGE_OUTPUT_K = 20

# Multi-Query 配额
PER_ENTITY_BM25_K = 15
PER_ENTITY_VEC_K = 5
MIN_PER_ENTITY = 3
TOTAL_POOL_K = 200  # 大候选池


# ─── 工具函数 ───

def load_test_questions(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]

def load_chunk_meta_map():
    client = chromadb.PersistentClient(path=get_abs_path("chroma_db"))
    collection = client.get_collection(chroma_conf["collection_name"])
    all_data = collection.get(include=["metadatas"], limit=5000)
    return {m["chunk_id"]: m for m in all_data["metadatas"] if m.get("chunk_id")}

def doc_matches_source(doc, filename_contains):
    fn = filename_contains.lower()
    return (fn in doc.metadata.get("source_file", "").lower()
            or fn in doc.metadata.get("paper_id", "").lower()
            or fn in doc.metadata.get("paper_title", "").lower())

def doc_matches_source_and_page(doc, fn, pages):
    if not doc_matches_source(doc, fn):
        return False
    ps = doc.metadata.get("page_start")
    pe = doc.metadata.get("page_end")
    if ps is None:
        ps = pe = doc.metadata.get("page")
    if ps is None:
        return False
    return any(int(ps) <= p <= int(pe) for p in pages)


# ─── 指标函数 ───

def compute_source_recall_at_k(retrieved, expected_sources, k):
    if not expected_sources: return None
    top_k = retrieved[:k]
    hit = set()
    for es in expected_sources:
        fn = es.get("filename_contains", "")
        if not fn: continue
        for doc in top_k:
            if doc_matches_source(doc, fn):
                hit.add(fn.lower())
                break
    return len(hit) / len(expected_sources)

def compute_evidence_recall_at_k(retrieved, expected_sources, k):
    if not expected_sources: return None
    top_k = retrieved[:k]
    hit = 0
    for es in expected_sources:
        fn = es.get("filename_contains", "")
        pages = es.get("pages_any", [])
        if not fn: continue
        for doc in top_k:
            if doc_matches_source_and_page(doc, fn, pages):
                hit += 1
                break
    return hit / len(expected_sources)

def compute_source_hit_at_k(retrieved, expected_sources, k):
    if not expected_sources: return None
    for doc in retrieved[:k]:
        for es in expected_sources:
            fn = es.get("filename_contains", "")
            if fn and doc_matches_source(doc, fn):
                return 1.0
    return 0.0

def compute_all_sources_hit_at_k(retrieved, expected_sources, k):
    if not expected_sources: return None
    top_k = retrieved[:k]
    for es in expected_sources:
        fn = es.get("filename_contains", "")
        if not fn: continue
        if not any(doc_matches_source(doc, fn) for doc in top_k):
            return 0.0
    return 1.0

def compute_source_mrr(retrieved, expected_sources):
    if not expected_sources: return None
    for rank, doc in enumerate(retrieved, 1):
        for es in expected_sources:
            fn = es.get("filename_contains", "")
            if fn and doc_matches_source(doc, fn):
                return 1.0 / rank
    return 0.0

def compute_keyword_coverage_at_k(retrieved, must_contain, k):
    if not must_contain: return None
    top_k_text = " ".join(d.page_content for d in retrieved[:k]).lower()
    hits = sum(1 for kw in must_contain if kw.lower() in top_k_text)
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


# ─── Multi-Query 候选池构建 ───

def build_mq_pool(subqueries, bm25, vs, total_k=TOTAL_POOL_K):
    """per-entity quota 构建大候选池（200 docs）"""
    entity_docs = defaultdict(OrderedDict)  # entity → OrderedDict[chunk_id → doc]

    for sq in subqueries:
        entity = sq["entity"]
        query = sq["query"]

        # BM25
        try:
            for d, score in bm25.search(query, PER_ENTITY_BM25_K):
                cid = d.metadata.get("chunk_id", "")
                if cid and cid not in entity_docs[entity]:
                    d.metadata["_bm25_score"] = score
                    entity_docs[entity][cid] = d
        except Exception:
            pass

        # Vector
        try:
            for d in vs.vector_store.as_retriever(search_kwargs={"k": PER_ENTITY_VEC_K}).invoke(query):
                cid = d.metadata.get("chunk_id", "")
                if cid and cid not in entity_docs[entity]:
                    d.metadata["_bm25_score"] = 0.0
                    entity_docs[entity][cid] = d
        except Exception:
            pass

    # 每 entity 内部按 BM25 排序
    for entity in entity_docs:
        sorted_docs = sorted(entity_docs[entity].values(),
                           key=lambda d: d.metadata.get("_bm25_score", 0), reverse=True)
        entity_docs[entity] = OrderedDict((d.metadata.get("chunk_id", ""), d) for d in sorted_docs)

    # Round-robin 合并
    entities = list(entity_docs.keys())
    iters = {e: iter(entity_docs[e].values()) for e in entities}
    counts = {e: 0 for e in entities}
    merged, seen = [], set()

    # Phase 1: MIN_PER_ENTITY
    while any(counts[e] < MIN_PER_ENTITY for e in entities) and len(merged) < total_k:
        for e in entities:
            if counts[e] >= MIN_PER_ENTITY: continue
            try:
                doc = next(iters[e])
                cid = doc.metadata.get("chunk_id", "")
                if cid not in seen:
                    merged.append(doc); seen.add(cid); counts[e] += 1
            except StopIteration:
                counts[e] = max(counts[e], MIN_PER_ENTITY)

    # Phase 2: fill to total_k
    while len(merged) < total_k:
        added = False
        for e in entities:
            if len(merged) >= total_k: break
            try:
                doc = next(iters[e])
                cid = doc.metadata.get("chunk_id", "")
                if cid not in seen:
                    merged.append(doc); seen.add(cid); added = True
            except StopIteration:
                pass
        if not added:
            break

    return merged[:total_k]


# ─── 主流程 ───

def run_eval():
    all_questions = load_test_questions(EVAL_PATH)
    os.makedirs(REPORT_DIR, exist_ok=True)

    # Load multi-query cache
    with open(MULTI_CACHE_PATH) as f:
        multi_cache = json.load(f)
    print(f"Multi-Query 缓存：{len(multi_cache)} 条")

    answerable = [q for q in all_questions if q.get("should_answer", True)]
    unanswerable = [q for q in all_questions if not q.get("should_answer", True)]
    print(f"加载 {len(all_questions)} 题：可答 {len(answerable)}，不可答 {len(unanswerable)}")

    chunk_meta_map = load_chunk_meta_map()
    print(f"Chunk 元数据：{len(chunk_meta_map)} 条")

    # Init
    vs = VectorStoreService()
    bm25 = BM25Store()
    bm25.load()
    bm25.add_domain_terms()

    # Pre-build MQ pools for all answerable questions
    mq_pools = {}    # qid → list[Document]
    mq_subqueries = {}  # qid → subqueries list
    for q in answerable:
        qid = q["id"]
        plan = multi_cache.get(qid)
        if plan and plan.get("subqueries"):
            mq_pools[qid] = build_mq_pool(plan["subqueries"], bm25, vs, TOTAL_POOL_K)
            mq_subqueries[qid] = plan["subqueries"]
        else:
            # fallback: single query
            mq_pools[qid] = [d for d, _ in bm25.search(q["question"], TOTAL_POOL_K)]
            mq_subqueries[qid] = [{"entity": "fallback", "query": q["question"]}]
    print(f"MQ 候选池预构建完成：{len(mq_pools)} 题")

    # Reranker variants
    reranker_baseline = Reranker()
    reranker_enhanced = Reranker(passage_mode=True)
    reranker_fusion_07 = Reranker(passage_mode=True, fusion_enabled=True, alpha=0.7)
    reranker_fusion_08 = Reranker(passage_mode=True, fusion_enabled=True, alpha=0.8)
    reranker_bm25_large = Reranker(passage_mode=True, fusion_enabled=False)
    reranker_hybrid_large = Reranker(passage_mode=True, fusion_enabled=True, alpha=0.7)
    hybrid_scorer = HybridScorer(bm25_store=bm25, reranker=Reranker(passage_mode=True, fusion_enabled=False))

    # Build strategy functions — each takes (qid, question_dict, pool, first_subquery)
    # pool = pre-built multi-query candidate docs

    def make_strategies():
        return OrderedDict([
            ("mq_pool@50", lambda pool, sq: pool[:50]),
            ("mq_pool@100", lambda pool, sq: pool[:100]),
            ("mq_pool@200", lambda pool, sq: pool[:200]),
            ("mq_rerank@8", lambda pool, sq: reranker_baseline.rerank(sq, pool[:EVAL_RERANK_INPUT_K], top_k=8)),
            ("mq_rerank@20", lambda pool, sq: reranker_baseline.rerank(sq, pool[:EVAL_RERANK_LARGE_INPUT_K], top_k=20)),
            ("mq_fusion07@8", lambda pool, sq: reranker_fusion_07.rerank(sq, pool[:EVAL_RERANK_INPUT_K], top_k=8)),
            ("mq_fusion07@20", lambda pool, sq: reranker_fusion_07.rerank(sq, pool[:EVAL_RERANK_LARGE_INPUT_K], top_k=20)),
            ("mq_fusion08@8", lambda pool, sq: reranker_fusion_08.rerank(sq, pool[:EVAL_RERANK_INPUT_K], top_k=8)),
            ("mq_hybrid_score", lambda pool, sq: hybrid_scorer.retrieve(sq, bm25_k=min(len(pool), 50), top_k=20)),
        ])

    strategies = make_strategies()

    # Accumulators
    result_answerable = {name: defaultdict(list) for name in strategies}
    result_unanswerable = {name: defaultdict(list) for name in strategies}

    # Staged recall (from mq pool stages)
    staged_answerable = defaultdict(lambda: defaultdict(list))
    stage_configs = [
        ("mq_bm25_30", 30, "MQ per-entity BM25 top-30"),
        ("mq_bm25_50", 50, "MQ per-entity BM25 top-50"),
        ("mq_pool_50", 50, "MQ round-robin pool top-50"),
        ("mq_pool_100", 100, "MQ round-robin pool top-100"),
        ("mq_pool_200", 200, "MQ round-robin pool top-200"),
        ("mq_rerank_5", 5, "MQ → Reranker(fusion) top-5"),
        ("mq_rerank_10", 10, "MQ → Reranker(fusion) top-10"),
        ("mq_rerank_20", 20, "MQ → Reranker(fusion) top-20"),
    ]

    category_stats = defaultdict(lambda: defaultdict(list))

    for qset, result_bucket, label in [
        (answerable, result_answerable, "answerable"),
        (unanswerable, result_unanswerable, "unanswerable"),
    ]:
        for ii, q in enumerate(qset, 1):
            qid = q["id"]
            query = q["question"]
            expected = q.get("expected_sources", [])
            must_contain = q.get("must_contain", [])
            expected_chunk_ids = q.get("expected_chunk_ids", [])
            pool = mq_pools.get(qid, [])
            first_sq = mq_subqueries.get(qid, [{"entity": "?", "query": query}])[0]["query"]

            print(f"[{label} {ii}/{len(qset)}] {qid} pool={len(pool)}")

            # ── 分阶段召回 ──
            if label == "answerable" and _normalize_chunk_groups(expected_chunk_ids):
                for stage_name, stage_k, _desc in stage_configs:
                    if stage_name.startswith("mq_bm25_"):
                        # Build BM25 pool from subqueries only (no vector)
                        bm25_pool = []
                        bm25_seen = set()
                        for sq in mq_subqueries.get(qid, []):
                            try:
                                for d, _ in bm25.search(sq["query"], PER_ENTITY_BM25_K):
                                    cid = d.metadata.get("chunk_id", "")
                                    if cid and cid not in bm25_seen:
                                        bm25_pool.append(d); bm25_seen.add(cid)
                            except Exception:
                                pass
                        docs = bm25_pool[:stage_k]
                    elif stage_name.startswith("mq_rerank_"):
                        try:
                            docs = reranker_fusion_07.rerank(first_sq, pool[:EVAL_RRF_OUTPUT_K], top_k=stage_k)
                        except Exception:
                            docs = pool[:stage_k]
                    else:
                        docs = pool[:stage_k]

                    sr, wr = compute_strict_chunk_recall_at_k(docs, expected_chunk_ids, stage_k), None
                    wr = compute_window_chunk_recall_at_k(docs, expected_chunk_ids, stage_k, chunk_meta_map)
                    if sr is not None: staged_answerable[stage_name]["strict"].append(sr)
                    if wr is not None: staged_answerable[stage_name]["window"].append(wr)

            # ── 主策略 ──
            for name, fn in strategies.items():
                try:
                    retrieved = fn(pool, first_sq)
                except Exception as e:
                    logger.warning(f"[MQ-Eval]{name} {qid} 失败：{e}")
                    retrieved = []

                for k in K_VALUES:
                    for val, key in [
                        (compute_source_recall_at_k(retrieved, expected, k), f"source_recall@{k}"),
                        (compute_evidence_recall_at_k(retrieved, expected, k), f"evidence_recall@{k}"),
                        (compute_source_hit_at_k(retrieved, expected, k), f"source_hit@{k}"),
                        (compute_all_sources_hit_at_k(retrieved, expected, k), f"all_sources_hit@{k}"),
                        (compute_keyword_coverage_at_k(retrieved, must_contain, k), f"keyword_coverage@{k}"),
                        (compute_strict_chunk_recall_at_k(retrieved, expected_chunk_ids, k), f"strict_chunk_recall@{k}"),
                        (compute_window_chunk_recall_at_k(retrieved, expected_chunk_ids, k, chunk_meta_map), f"window_chunk_recall@{k}"),
                    ]:
                        if val is not None:
                            result_bucket[name][key].append(val)

                mrr = compute_source_mrr(retrieved, expected)
                if mrr is not None:
                    result_bucket[name]["source_mrr"].append(mrr)

                # Category stats (use mq_fusion07@8)
                if name == "mq_fusion07@8" and label == "answerable":
                    cat = q.get("answer_type", "other")
                    for k in [20]:
                        scr = compute_strict_chunk_recall_at_k(retrieved, expected_chunk_ids, k)
                        wcr = compute_window_chunk_recall_at_k(retrieved, expected_chunk_ids, k, chunk_meta_map)
                        sr = compute_source_recall_at_k(retrieved, expected, k)
                        er = compute_evidence_recall_at_k(retrieved, expected, k)
                        m = compute_source_mrr(retrieved, expected)
                        if scr is not None: category_stats[cat]["strict_chunk_recall@20"].append(scr)
                        if wcr is not None: category_stats[cat]["window_chunk_recall@20"].append(wcr)
                        if sr is not None: category_stats[cat]["source_recall@20"].append(sr)
                        if er is not None: category_stats[cat]["evidence_recall@20"].append(er)
                        if m is not None: category_stats[cat]["source_mrr"].append(m)

    # ─── 写报告 ───
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    report_path = os.path.join(REPORT_DIR, f"multi_query_ablation_{ts}.md")

    report = []
    w = report.append
    w("# Multi-Query 检索策略消融评估报告")
    w("")
    w(f"**评估时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    w(f"**数据集**: `rag_eval_20.jsonl` ({len(answerable)} answerable)")
    w(f"**Multi-Query 配额**: per-entity BM25={PER_ENTITY_BM25_K}, Vector={PER_ENTITY_VEC_K}, min={MIN_PER_ENTITY}, pool={TOTAL_POOL_K}")
    w(f"**K_VALUES**: {K_VALUES}")
    w(f"**候选池**: Multi-Query → round-robin {TOTAL_POOL_K} docs → 各策略后处理")
    w("")

    # ── 分阶段召回 ──
    w("## 分阶段召回统计（strict / window chunk_recall）")
    w("")
    w("| 阶段 | strict_chunk_recall | window_chunk_recall | 说明 |")
    w("|------|-------------------|-------------------|------|")
    stages_display = [
        ("mq_bm25_30", "MQ-BM25 @30", "per-entity BM25 合并 top-30"),
        ("mq_bm25_50", "MQ-BM25 @50", "per-entity BM25 合并 top-50"),
        ("mq_pool_50", "MQ Pool @50", "round-robin pool top-50"),
        ("mq_pool_100", "MQ Pool @100", "round-robin pool top-100"),
        ("mq_pool_200", "MQ Pool @200", "round-robin pool top-200"),
        ("mq_rerank_5", "MQ Rerank @5", "pool→Reranker(fusion) top-5"),
        ("mq_rerank_10", "MQ Rerank @10", "pool→Reranker(fusion) top-10"),
        ("mq_rerank_20", "MQ Rerank @20", "pool→Reranker(fusion) top-20"),
    ]
    for key, label, desc in stages_display:
        sv = staged_answerable.get(key, {}).get("strict", [])
        wv = staged_answerable.get(key, {}).get("window", [])
        avg_s = sum(sv) / len(sv) if sv else 0.0
        avg_w = sum(wv) / len(wv) if wv else 0.0
        w(f"| {label} | {avg_s:.3f} | {avg_w:.3f} | {desc} |")
    w("")

    # ── 主策略指标 ──
    w("## 可答题检索指标（Multi-Query 全策略）")
    w("")
    strat_names = list(strategies.keys())
    header = "| 指标 | " + " | ".join(sn.replace("|", "\\|") for sn in strat_names) + " |"
    sep = "|------|" + "|".join("-" * (len(n) + 2) for n in strat_names) + "|"
    w(header)
    w(sep)

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
        for name in strat_names:
            scores = result_answerable[name].get(metric, [])
            vals[name] = sum(scores) / len(scores) if scores else 0.0
        row = "| " + metric + " | " + " | ".join(f"{vals[n]:.3f}" for n in strat_names) + " |"
        best = max(vals, key=vals.get)
        row += f" 🏆 {best}"
        w(row)
    w("")

    # ── 分类统计 ──
    w("## 按题型分类统计（mq_fusion07@8 @20）")
    w("")
    w("| 类别 | 题数 | source_recall | evidence_recall | source_mrr | strict_chunk | window_chunk |")
    w("|------|------|-------------|---------------|-----------|-------------|-------------|")
    for cat in sorted(category_stats.keys()):
        stats = category_stats[cat]
        n = len(stats.get("strict_chunk_recall@20", []))
        if n == 0: continue
        avg_src = sum(stats.get("source_recall@20",[])) / n
        avg_evd = sum(stats.get("evidence_recall@20",[])) / n
        avg_mrr = sum(stats.get("source_mrr",[])) / n
        avg_s = sum(stats.get("strict_chunk_recall@20",[])) / n
        avg_w = sum(stats.get("window_chunk_recall@20",[])) / n
        w(f"| {cat} | {n} | {avg_src:.3f} | {avg_evd:.3f} | {avg_mrr:.3f} | {avg_s:.3f} | {avg_w:.3f} |")
    w("")

    # ── 逐题详情 ──
    w("## 逐题详情（可答题）")
    w("")
    for q in answerable:
        qid = q["id"]
        expected_ids = q.get("expected_chunk_ids", [])
        pool = mq_pools.get(qid, [])
        # 取 mq_fusion07@8 结果
        try:
            retrieved = strategies["mq_fusion07@8"][1](pool, mq_subqueries.get(qid, [{"query": q["question"]}])[0]["query"])
        except Exception:
            retrieved = pool[:8]
        s5 = compute_strict_chunk_recall_at_k(retrieved, expected_ids, 5)
        s20 = compute_strict_chunk_recall_at_k(retrieved, expected_ids, 20)
        w(f"- **{qid}** [{q.get('answer_type','')}] pool={len(pool)} strict@5={(s5 or 0):.2f} strict@20={(s20 or 0):.2f}")
    w("")

    full = "\n".join(report)
    print("\n" + full)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(full)
    print(f"报告已保存至：{report_path}")


if __name__ == "__main__":
    run_eval()

def main(argv=None) -> int:
    """CLI 入口"""
    run_eval()
    return 0
