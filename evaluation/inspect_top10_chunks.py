"""
输出 Per-Subquery 策略的 top-10 chunk 完整内容。

用法：python evaluation/inspect_top10_chunks.py
输出：evaluation/reports/top10_chunks_<timestamp>.md
"""
import sys, os, json
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.bm25_store import BM25Store
from rag.retrieval_strategy import Reranker, HybridScorer
from utils.path_tool import get_abs_path

EVAL_PATH = get_abs_path("evaluation/rag_eval_20.jsonl")
MULTI_CACHE_PATH = get_abs_path("evaluation/multi_query_cache.json")
OUTPUT_DIR = get_abs_path("evaluation/reports")

BM25_K = 50
FINAL_TOP_K = 10
PER_ENTITY_MIN = 3
BM25_LARGE_K = 200


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


def format_content(text: str) -> str:
    """截断过长内容，保留关键部分"""
    if len(text) <= 3000:
        return text
    return text[:3000] + f"\n\n... [truncated, total {len(text)} chars]"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Init
    bm25 = BM25Store()
    bm25.load()
    bm25.add_domain_terms()
    hyb_scorer = HybridScorer(bm25_store=bm25, reranker=Reranker(passage_mode=True, fusion_enabled=False))

    # Load questions & multi-query cache
    with open(EVAL_PATH) as f:
        questions = [json.loads(l) for l in f if l.strip()]

    with open(MULTI_CACHE_PATH) as f:
        multi_cache = json.load(f)

    answerable = [q for q in questions if q.get("should_answer") and q.get("expected_chunk_ids")]
    unanswerable = [q for q in questions if not q.get("should_answer")]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = os.path.join(OUTPUT_DIR, f"top10_chunks_{timestamp}.md")

    with open(output_path, "w", encoding="utf-8") as f:
        w = f.write
        w("# Per-Subquery + 实体保底策略 Top-10 Chunks 详情\n\n")
        w(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        w(f"**数据集**: `rag_eval_20.jsonl` ({len(answerable)} answerable + {len(unanswerable)} unanswerable)  \n")
        w(f"**策略**: Phase1 每 entity 约束检索（保底 {PER_ENTITY_MIN} 条）→ Phase2 全局 HybridScorer → Phase3 合并 → Top-{FINAL_TOP_K}  \n")
        w(f"**权重**: BM25=0.45, Reranker=0.25, Keyword=0.20, Metadata=0.10 | bm25_large_k={BM25_LARGE_K}  \n\n")
        w("---\n\n")

        for q in answerable + unanswerable:
            qid = q["id"]
            question = q["question"]
            mq_plan = multi_cache.get(qid, {"subqueries": [{"entity": "fallback", "query": question}]})
            expected_ids = q.get("expected_chunk_ids", [])

            w(f"## {qid}\n\n")
            w(f"**Question**: {question}  \n")
            w(f"**Type**: {q.get('answer_type', 'N/A')} | **Should Answer**: {q.get('should_answer', True)}  \n")

            # Multi-query plan
            w(f"**Entities**: {mq_plan.get('entities', [])}  \n")
            w(f"**Subqueries**:  \n")
            for sq in mq_plan.get("subqueries", []):
                w(f"  - [{sq['entity']}] {sq['query']}  \n")
            w(f"**Expected Chunk IDs**: {expected_ids}  \n\n")

            # Run per-subquery 策略
            subqueries = mq_plan.get("subqueries", [])
            if not subqueries:
                subqueries = [{"entity": "fallback", "query": question}]

            try:
                top10 = per_subquery_retrieve(subqueries, hyb_scorer, FINAL_TOP_K)
                # 分数仅用于展示，用第一条 subquery 算 HybridScorer 得分
                first_sq = subqueries[0]["query"]
                bm25_results = {d.metadata.get("chunk_id", ""): s for d, s in bm25.search(first_sq, BM25_K)}
                rerank_scores = hyb_scorer.reranker.score_batch(first_sq, top10)
                top10_scores = {}
                for i, d in enumerate(top10):
                    cid = d.metadata.get("chunk_id", "")
                    kw = hyb_scorer._keyword_overlap(first_sq, d.page_content)
                    meta = hyb_scorer._metadata_boost(first_sq, d)
                    top10_scores[i] = (
                        hyb_scorer.w_bm25 * bm25_results.get(cid, 0)
                        + hyb_scorer.w_rerank * rerank_scores.get(i, 0)
                        + hyb_scorer.w_keyword * kw
                        + hyb_scorer.w_metadata * meta
                    )
            except Exception as e:
                w(f"  ⚠️ Per-subquery retrieval failed: {e}\n\n")
                top10 = []
                top10_scores = {}

            # Output top-10 chunks
            w(f"### Top-10 Per-Subquery Chunks (共 {len(subqueries)} 条 subquery)\n\n")

            # Flatten grouped expected_chunk_ids for HIT marking
            flat_expected = set()
            for item in expected_ids:
                if isinstance(item, list):
                    flat_expected.update(item)
                else:
                    flat_expected.add(item)

            for rank, doc in enumerate(top10, 1):
                meta = doc.metadata
                cid = meta.get("chunk_id", "N/A")
                source = meta.get("source_file", "N/A")
                section = meta.get("section", "N/A")
                page_start = meta.get("page_start", "?")
                page_end = meta.get("page_end", "?")
                chunk_idx = meta.get("chunk_index", "?")
                paper_title = meta.get("paper_title", source)

                is_expected = "✅" if cid in flat_expected else ""
                hit_label = f" **HIT**" if is_expected else ""

                w(f"#### #{rank}{hit_label} — `{cid}` — {paper_title}  \n")
                w(f"**Score**: {top10_scores.get(rank-1, 0):.4f} | "
                  f"**Section**: {section} | **Page**: {page_start}–{page_end} | "
                  f"**Chunk Index**: {chunk_idx} | {is_expected}  \n\n")

                w("```text\n")
                w(format_content(doc.page_content))
                w("\n```\n\n")

                # 元数据折叠
                w("<details>\n<summary>完整 metadata</summary>\n\n")
                w("```json\n")
                w(json.dumps({k: v for k, v in meta.items()
                              if k != "page_content"}, ensure_ascii=False, indent=2))
                w("\n```\n</details>\n\n")

            w("---\n\n")

    print(f"Done → {output_path}")


if __name__ == "__main__":
    main()
