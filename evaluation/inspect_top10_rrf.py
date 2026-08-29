"""
RRF 策略下每个问题的 top-10 chunk 完整内容。

用法：python evaluation/inspect_top10_rrf.py
输出：evaluation/reports/top10_rrf_<timestamp>.md
"""
import sys, os, json
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.bm25_store import BM25Store
from rag.retrieval_strategy import Reranker, HybridScorer
from utils.path_tool import get_abs_path
from evaluation.multi_query_eval import multi_query_retrieve, init_retrievers

EVAL_PATH = get_abs_path("evaluation/rag_eval_20.jsonl")
MULTI_CACHE_PATH = get_abs_path("evaluation/multi_query_cache.json")
OUTPUT_DIR = get_abs_path("evaluation/reports")

FINAL_TOP_K = 10
RRF_K = 60


def rrf_retrieve(subqueries, mq_pool, hyb_scorer, bm25, top_k=10):
    """Phase 2: Per-Subquery 打分 → RRF 排名融合 → BM25 保底 → Top-K"""
    # Per-subquery HybridScorer 打分
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
    rrf_scores = {}
    rrf_details = {}  # {chunk_idx: [(subquery_idx, rank, raw_score)]}
    for sq_idx, sq_scores in enumerate(all_subq_scores):
        ranked = sorted(sq_scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (i, raw_score) in enumerate(ranked, 1):
            rrf_scores[i] = rrf_scores.get(i, 0) + 1.0 / (RRF_K + rank)
            if i not in rrf_details:
                rrf_details[i] = []
            rrf_details[i].append((sq_idx, rank, raw_score))

    # BM25 safeguard
    bm25_max = {i: max(bs[i] for bs in all_subq_bm25) for i in range(len(mq_pool))}
    bm25_top5 = {i for i, _ in sorted(bm25_max.items(), key=lambda x: x[1], reverse=True)[:5]}

    # Select top-K
    ranking = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    selected = []
    seen = set()
    for i, _ in ranking:
        if len(selected) >= top_k:
            break
        if i not in seen:
            selected.append((i, rrf_scores[i], rrf_details.get(i, [])))
            seen.add(i)
    for i in sorted(bm25_top5):
        if i not in seen and len(selected) < top_k:
            selected.append((i, rrf_scores.get(i, 0), rrf_details.get(i, [])))

    return [(mq_pool[i], rrf_score, details) for i, rrf_score, details in selected[:top_k]]


def format_content(text: str) -> str:
    if len(text) <= 3000:
        return text
    return text[:3000] + f"\n\n... [truncated, total {len(text)} chars]"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Init
    vs, bm25, hyb_scorer = init_retrievers()

    # Load data
    with open(EVAL_PATH) as f:
        questions = [json.loads(l) for l in f if l.strip()]
    with open(MULTI_CACHE_PATH) as f:
        multi_cache = json.load(f)

    answerable = [q for q in questions if q.get("should_answer") and q.get("expected_chunk_ids")]
    unanswerable = [q for q in questions if not q.get("should_answer")]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = os.path.join(OUTPUT_DIR, f"top10_rrf_{timestamp}.md")

    with open(output_path, "w", encoding="utf-8") as f:
        w = f.write
        w("# RRF 策略 Top-10 Chunks 详情\n\n")
        w(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        w(f"**数据集**: `rag_eval_20.jsonl` ({len(answerable)} answerable + {len(unanswerable)} unanswerable)  \n")
        w(f"**策略**: MQ Pool → Per-Subquery HybridScorer → RRF(k={RRF_K}) 排名融合 → BM25 保底(top-5) → Top-{FINAL_TOP_K}  \n")
        w(f"**权重**: BM25=0.45, Reranker=0.25, Keyword=0.20, Metadata=0.10  \n\n")
        w("---\n\n")

        for q in answerable + unanswerable:
            qid = q["id"]
            question = q["question"]
            mq_plan = multi_cache.get(qid, {"subqueries": [{"entity": "fallback", "query": question}]})
            expected_ids = q.get("expected_chunk_ids", [])

            w(f"## {qid}\n\n")
            w(f"**Question**: {question}  \n")
            w(f"**Type**: {q.get('answer_type', 'N/A')} | **Should Answer**: {q.get('should_answer', True)}  \n")
            w(f"**Entities**: {mq_plan.get('entities', [])}  \n")
            w(f"**Subqueries**:  \n")
            for sq in mq_plan.get("subqueries", []):
                w(f"  - [{sq['entity']}] {sq['query']}  \n")

            # Flatten expected for HIT marking
            flat_expected = set()
            for item in expected_ids:
                if isinstance(item, list):
                    flat_expected.update(item)
                else:
                    flat_expected.add(item)
            w(f"**Expected Chunk IDs**: {expected_ids}  \n\n")

            subqueries = mq_plan.get("subqueries", [])
            if not subqueries:
                subqueries = [{"entity": "fallback", "query": question}]

            try:
                mq_pool = multi_query_retrieve(subqueries, bm25, vs, hyb_scorer)
                if not mq_pool:
                    w("  ⚠️ MQ pool empty\n\n---\n\n")
                    continue
                top10 = rrf_retrieve(subqueries, mq_pool, hyb_scorer, bm25, FINAL_TOP_K)
            except Exception as e:
                w(f"  ⚠️ RRF retrieval failed: {e}\n\n---\n\n")
                continue

            w(f"### Top-10 RRF Chunks (pool={len(mq_pool)}, subqueries={len(subqueries)})\n\n")

            for rank, (doc, rrf_score, details) in enumerate(top10, 1):
                meta = doc.metadata
                cid = meta.get("chunk_id", "N/A")
                source = meta.get("source_file", "N/A")
                section = meta.get("section", "N/A")
                page_start = meta.get("page_start", "?")
                page_end = meta.get("page_end", "?")
                paper_title = meta.get("paper_title", source)

                is_hit = cid in flat_expected
                hit_label = " **HIT**" if is_hit else ""

                # Subquery ranking details
                sq_info = []
                for sq_idx, sq_rank, raw_score in sorted(details, key=lambda x: x[1]):
                    sq_name = subqueries[sq_idx]["entity"][:15] if sq_idx < len(subqueries) else "?"
                    sq_info.append(f"sq{sq_idx+1}[{sq_name}] rank=#{sq_rank} raw={raw_score:.4f}")
                sq_str = " | ".join(sq_info)

                w(f"#### #{rank}{hit_label} — `{cid}`\n")
                w(f"**RRF Score**: {rrf_score:.4f} | **Paper**: {paper_title[:80]}  \n")
                w(f"**Section**: {section} | **Page**: {page_start}–{page_end}  \n")
                w(f"**Per-Subquery**: {sq_str}  \n")
                if is_hit:
                    w(f"**Status**: ✅ HIT  \n")
                w("\n```text\n")
                w(format_content(doc.page_content))
                w("\n```\n\n")

                w("<details>\n<summary>完整 metadata</summary>\n\n```json\n")
                w(json.dumps({k: v for k, v in meta.items()
                              if k != "page_content"}, ensure_ascii=False, indent=2))
                w("\n```\n</details>\n\n")

            w("---\n\n")

    print(f"Done → {output_path}")


if __name__ == "__main__":
    main()
