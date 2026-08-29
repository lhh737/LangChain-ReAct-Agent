"""
Per-Subquery + 实体保底 vs Single-Subquery Baseline 对比评估

策略:
  baseline: 第一条 subquery → HybridScorer.retrieve(bm25_k=50, top_k=K)
  per_subq: Phase1 每 entity 约束 BM25(200) → HybridScorer 保底 3 条
            → Phase2 全局 HybridScorer → Phase3 合并 → top-K

用法: python evaluation/per_subquery_eval.py
输出: evaluation/reports/per_subquery_eval_<timestamp>.md
"""
import sys, os, json
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb

from rag.bm25_store import BM25Store
from rag.retrieval_strategy import Reranker, HybridScorer
from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path

EVAL_PATH = get_abs_path("evaluation/rag_eval_20.jsonl")
MULTI_CACHE_PATH = get_abs_path("evaluation/multi_query_cache.json")
REPORT_DIR = get_abs_path("evaluation/reports")

BM25_K = 50
BM25_LARGE_K = 200
PER_ENTITY_MIN = 3
K_VALUES = [5, 10, 20]


# ─── 工具函数 ───

def _normalize_chunk_groups(expected_chunk_ids):
    if not expected_chunk_ids:
        return []
    if isinstance(expected_chunk_ids[0], list):
        return expected_chunk_ids
    return [[cid] for cid in expected_chunk_ids]


def doc_matches_source(doc, filename_fragment):
    return filename_fragment.lower() in (doc.metadata.get("source_file", "") or "").lower()


def load_chunk_meta_map():
    client = chromadb.PersistentClient(path=get_abs_path("chroma_db"))
    collection = client.get_collection(chroma_conf["collection_name"])
    all_data = collection.get(include=["metadatas"], limit=5000)
    return {m["chunk_id"]: m for m in all_data["metadatas"] if m.get("chunk_id")}


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
        if any(d.metadata.get("chunk_id", "") in group for d in retrieved_slice):
            hits += 1
            continue
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


def compute_entity_coverage_at_k(retrieved, subqueries, k):
    """Top-K 中覆盖了多少个 entity（每个 entity 至少 1 个 chunk）"""
    entities = list({sq["entity"] for sq in subqueries})
    if len(entities) <= 1:
        return None  # 只有 1 个 entity 时无意义
    top_k = retrieved[:k]
    covered = set()
    for d in top_k:
        source = (d.metadata.get("source_file", "") or "").lower()
        paper_title = (d.metadata.get("paper_title", "") or "").lower()
        for e in entities:
            el = e.lower()
            if el in source or el in paper_title:
                covered.add(e)
    return len(covered) / len(entities)


# ─── 检索策略 ───

def baseline_retrieve(subqueries, hyb_scorer, top_k):
    """当前 mq_hybrid_score：仅用第一条 subquery"""
    first_sq = subqueries[0]["query"] if subqueries else ""
    if not first_sq:
        return []
    try:
        return hyb_scorer.retrieve(first_sq, bm25_k=BM25_K, top_k=top_k)
    except Exception:
        return []


def _entity_name_in_paper(doc, entity):
    """chunk 是否属于该 entity 的论文"""
    el = entity.lower()
    source = (doc.metadata.get("source_file", "") or "").lower()
    title = (doc.metadata.get("paper_title", "") or "").lower()
    return el in source or el in title


def per_subquery_retrieve(subqueries, hyb_scorer, final_k):
    """Phase 1: 每 entity 约束检索（保底）→ Phase 2: 全局检索 → Phase 3: 合并"""
    bm25 = hyb_scorer.bm25
    seen_ids = set()

    # ── Phase 1: 每 entity 实体约束检索，保底 PER_ENTITY_MIN 条 ──
    guaranteed = []
    for sq in subqueries:
        entity = sq["entity"]
        query = sq["query"]
        try:
            entity_candidates = []
            for d, s in bm25.search(query, BM25_LARGE_K):
                if _entity_name_in_paper(d, entity) and d.metadata.get("chunk_id", "") not in seen_ids:
                    d.metadata["_bm25_score"] = s
                    entity_candidates.append(d)
        except Exception:
            entity_candidates = []
        if not entity_candidates:
            continue
        entity_candidates = entity_candidates[:20]
        # HybridScorer 打分
        rerank_scores = hyb_scorer.reranker.score_batch(query, entity_candidates)
        scored = []
        for i, d in enumerate(entity_candidates):
            kw = hyb_scorer._keyword_overlap(query, d.page_content)
            meta = hyb_scorer._metadata_boost(query, d)
            score = (
                hyb_scorer.w_bm25 * d.metadata.get("_bm25_score", 0)
                + hyb_scorer.w_rerank * rerank_scores.get(i, 0)
                + hyb_scorer.w_keyword * kw
                + hyb_scorer.w_metadata * meta
            )
            scored.append((score, d))
        scored.sort(key=lambda x: x[0], reverse=True)
        for _, d in scored[:PER_ENTITY_MIN]:
            cid = d.metadata.get("chunk_id", "")
            if cid not in seen_ids:
                guaranteed.append(d)
                seen_ids.add(cid)

    # ── Phase 2: 全局检索（补齐到 final_k） ──
    first_sq = subqueries[0]["query"] if subqueries else ""
    try:
        global_docs = hyb_scorer.retrieve(first_sq, bm25_k=BM25_K, top_k=final_k * 2)
    except Exception:
        global_docs = []

    # ── Phase 3: 合并 ──
    merged = list(guaranteed)
    for d in global_docs:
        if len(merged) >= final_k:
            break
        cid = d.metadata.get("chunk_id", "")
        if cid not in seen_ids:
            merged.append(d)
            seen_ids.add(cid)

    return merged[:final_k]


# ─── 主流程 ───

def main():
    os.makedirs(REPORT_DIR, exist_ok=True)
    chunk_meta_map = load_chunk_meta_map()
    print(f"Chunk 元数据: {len(chunk_meta_map)} 条")

    # Init
    bm25 = BM25Store()
    bm25.load()
    bm25.add_domain_terms()
    hyb_scorer = HybridScorer(bm25_store=bm25, reranker=Reranker(passage_mode=True, fusion_enabled=False))

    # Load data
    with open(EVAL_PATH) as f:
        questions = [json.loads(l) for l in f if l.strip()]
    with open(MULTI_CACHE_PATH) as f:
        multi_cache = json.load(f)

    answerable = [q for q in questions if q.get("should_answer") and q.get("expected_chunk_ids")]

    # Per-question comparison
    rows = []
    for q in answerable:
        qid = q["id"]
        plan = multi_cache.get(qid, {"subqueries": [{"entity": "fallback", "query": q["question"]}]})
        subqueries = plan.get("subqueries", [])
        num_sq = len(subqueries)

        # Both strategies
        base_docs = baseline_retrieve(subqueries, hyb_scorer, max(K_VALUES))
        per_docs = per_subquery_retrieve(subqueries, hyb_scorer, max(K_VALUES))

        row = {
            "id": qid,
            "answer_type": q.get("answer_type", ""),
            "num_subqueries": num_sq,
            "entities": plan.get("entities", []),
        }

        for k in K_VALUES:
            for label, docs in [("base", base_docs), ("per", per_docs)]:
                s = compute_strict_chunk_recall_at_k(docs, q.get("expected_chunk_ids", []), k)
                w = compute_window_chunk_recall_at_k(docs, q.get("expected_chunk_ids", []), k, chunk_meta_map)
                src = compute_source_recall_at_k(docs, q.get("expected_sources", []), k)
                ec = compute_entity_coverage_at_k(docs, subqueries, k)
                row[f"{label}_strict@{k}"] = s
                row[f"{label}_window@{k}"] = w
                row[f"{label}_source@{k}"] = src
                if k == max(K_VALUES) and ec is not None:
                    row[f"{label}_entity_cov"] = ec

        rows.append(row)
        print(f"[{len(rows)}/{len(answerable)}] {qid} subqueries={num_sq}")

    # ─── 写报告 ───
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_path = os.path.join(REPORT_DIR, f"per_subquery_eval_{timestamp}.md")

    with open(report_path, "w", encoding="utf-8") as f:
        w = f.write
        w("# Per-Subquery HybridScorer 对比评估\n\n")
        w(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        w(f"**数据集**: `rag_eval_20.jsonl` ({len(answerable)} answerable)  \n")
        w(f"**Baseline**: 第一条 subquery → HybridScorer.retrieve(bm25_k={BM25_K})  \n")
        w(f"**Per-Subquery**: Phase1 每 entity 约束 BM25(k={BM25_LARGE_K}) → HybridScorer 保底 {PER_ENTITY_MIN} 条 → Phase2 全局 HybridScorer → Phase3 合并  \n")
        w(f"**k 值**: {K_VALUES}  \n\n")
        w("---\n\n")

        # ── 1. 全局平均 ──
        w("## 1. 全局平均指标\n\n")
        w("| k | base strict | per strict | Δ strict | base window | per window | Δ window | base source | per source | Δ source |\n")
        w("|---|-----------|----------|---------|-----------|----------|---------|-----------|----------|--------|\n")
        for k in K_VALUES:
            vals = {}
            for label in ["base", "per"]:
                for metric in ["strict", "window", "source"]:
                    key = f"{label}_{metric}@{k}"
                    scores = [r[key] for r in rows if r.get(key) is not None]
                    vals[key] = sum(scores) / len(scores) if scores else 0.0
            bsk = f"base_strict@{k}"
            psk = f"per_strict@{k}"
            bwk = f"base_window@{k}"
            pwk = f"per_window@{k}"
            bsrck = f"base_source@{k}"
            psrck = f"per_source@{k}"
            w(f"| {k} | {vals[bsk]:.4f} | {vals[psk]:.4f} | "
              f"{vals[psk] - vals[bsk]:+.4f} | "
              f"{vals[bwk]:.4f} | {vals[pwk]:.4f} | "
              f"{vals[pwk] - vals[bwk]:+.4f} | "
              f"{vals[bsrck]:.4f} | {vals[psrck]:.4f} | "
              f"{vals[psrck] - vals[bsrck]:+.4f} |\n")
        w("\n")

        # ── 2. Entity coverage ──
        w("## 2. Entity Coverage（多实体题，top-20）\n\n")
        w("| question | entities | base cov | per cov |\n")
        w("|----------|----------|---------|--------|\n")
        ec_rows = [r for r in rows if r.get("base_entity_cov") is not None or r.get("per_entity_cov") is not None]
        for r in ec_rows:
            w(f"| {r['id']} | {r['entities']} | {r.get('base_entity_cov', 0) or 0:.2f} | "
              f"{r.get('per_entity_cov', 0) or 0:.2f} |\n")
        if ec_rows:
            base_ec = [r["base_entity_cov"] for r in ec_rows if r.get("base_entity_cov") is not None]
            per_ec = [r["per_entity_cov"] for r in ec_rows if r.get("per_entity_cov") is not None]
            avg_base = sum(base_ec) / len(base_ec) if base_ec else 0
            avg_per = sum(per_ec) / len(per_ec) if per_ec else 0
            w(f"| **平均** | | **{avg_base:.2f}** | **{avg_per:.2f}** |\n")
        w("\n")

        # ── 3. 按 subquery 数量分组 ──
        w("## 3. 按 Subquery 数量分组\n\n")
        sq_groups = {1: [], 2: [], 3: []}
        for r in rows:
            n = min(r["num_subqueries"], 3)
            sq_groups[n].append(r)
        for n in [1, 2, 3]:
            group = sq_groups[n]
            if not group:
                continue
            w(f"### {n} subquer{'y' if n == 1 else 'ies'} ({len(group)} questions)\n\n")
            w("| k | base strict | per strict | Δ strict | base window | per window | Δ window |\n")
            w("|---|-----------|----------|---------|-----------|----------|--------|\n")
            for k in K_VALUES:
                vals = {}
                for label in ["base", "per"]:
                    for metric in ["strict", "window"]:
                        key = f"{label}_{metric}@{k}"
                        scores = [r[key] for r in group if r.get(key) is not None]
                        vals[key] = sum(scores) / len(scores) if scores else 0.0
                bsk = f"base_strict@{k}"
                psk = f"per_strict@{k}"
                bwk = f"base_window@{k}"
                pwk = f"per_window@{k}"
                w(f"| {k} | {vals[bsk]:.4f} | {vals[psk]:.4f} | "
                  f"{vals[psk] - vals[bsk]:+.4f} | "
                  f"{vals[bwk]:.4f} | {vals[pwk]:.4f} | "
                  f"{vals[pwk] - vals[bwk]:+.4f} |\n")
            w("\n")

        # ── 4. 逐题详情 ──
        w("## 4. 逐题详情\n\n")
        w("| question | sq | base s@10 | per s@10 | Δ s@10 | base s@20 | per s@20 | Δ s@20 | base w@10 | per w@10 | Δ w@10 |\n")
        w("|----------|----|----------|---------|--------|----------|---------|--------|----------|---------|--------|\n")
        for r in rows:
            bs10 = r.get("base_strict@10") or 0
            ps10 = r.get("per_strict@10") or 0
            bs20 = r.get("base_strict@20") or 0
            ps20 = r.get("per_strict@20") or 0
            bw10 = r.get("base_window@10") or 0
            pw10 = r.get("per_window@10") or 0
            w(f"| {r['id']} | {r['num_subqueries']} | "
              f"{bs10:.4f} | {ps10:.4f} | {ps10 - bs10:+.4f} | "
              f"{bs20:.4f} | {ps20:.4f} | {ps20 - bs20:+.4f} | "
              f"{bw10:.4f} | {pw10:.4f} | {pw10 - bw10:+.4f} |\n")

    print(f"\nReport → {report_path}")


if __name__ == "__main__":
    main()
