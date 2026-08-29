"""逐题 chunk_recall@k 诊断报告，输出 Markdown 到 evaluation/reports/"""
import sys, os, json
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.bm25_store import BM25Store
from rag.retrieval_strategy import Reranker, HybridScorer
from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path
import chromadb

EVAL_PATH = get_abs_path("evaluation/rag_eval_20.jsonl")
K_LIST = [1, 3, 5, 10, 20]
OUTPUT_DIR = get_abs_path("evaluation/reports")

# ─── helpers ───

def load_chunk_meta_map():
    client = chromadb.PersistentClient(path=get_abs_path("chroma_db"))
    collection = client.get_collection(chroma_conf["collection_name"])
    all_data = collection.get(include=["metadatas", "documents"], limit=5000)
    meta_map = {}
    for m, doc in zip(all_data["metadatas"], all_data["documents"]):
        cid = m.get("chunk_id", "")
        if cid:
            meta_map[cid] = {"meta": m, "content": doc}
    return meta_map


def compute_strict_chunk_recall_at_k(retrieved_ids, expected_ids, k):
    if not expected_ids:
        return None
    top_k = set(retrieved_ids[:k])
    hits = sum(1 for cid in expected_ids if cid in top_k)
    return hits / len(expected_ids)


def compute_window_chunk_recall_at_k(retrieved_docs, expected_ids, k, chunk_meta_map):
    if not expected_ids:
        return None
    hits = 0
    for cid in expected_ids:
        if any(d.metadata.get("chunk_id", "") == cid for d in retrieved_docs[:k]):
            hits += 1
            continue
        exp_meta = chunk_meta_map.get(cid, {}).get("meta", {})
        if not exp_meta:
            continue
        for d in retrieved_docs[:k]:
            dm = d.metadata
            if (dm.get("paper_id") == exp_meta.get("paper_id")
                and dm.get("section") == exp_meta.get("section")
                and abs(dm.get("chunk_index", -1) - exp_meta.get("chunk_index", -1)) <= 1
                and abs(dm.get("page_start", 0) - exp_meta.get("page_start", 0)) <= 1):
                hits += 1
                break
    return hits / len(expected_ids)


def detect_lang(qid: str) -> str:
    return "ZH" if qid.endswith("_zh") else "EN"


def fmt_chunk_meta(cid, cmap, indent=""):
    """单行摘要：chunk_id | file | p. | sec | ci"""
    info = cmap.get(cid)
    if not info:
        return f"{indent}{cid} [STALE]"
    m = info["meta"]
    return (f"{indent}{cid} | {m.get('source_file','')[:60]} | "
            f"p.{m.get('page_start','?')}-{m.get('page_end','?')} | "
            f"sec={m.get('section','?')} | ci={m.get('chunk_index','?')}")


def fmt_chunk_full(cid, cmap):
    """完整 chunk：元数据头 + 全文"""
    info = cmap.get(cid)
    if not info:
        return f"### {cid}\n\n**[STALE — 不在当前 ChromaDB 中]**\n"
    m = info["meta"]
    content = info["content"]
    header = (
        f"### {cid}\n\n"
        f"| Field | Value |\n|-------|-------|\n"
        f"| source_file | {m.get('source_file','?')} |\n"
        f"| section | {m.get('section','?')} |\n"
        f"| section_title | {m.get('section_title','?')} |\n"
        f"| page_start | {m.get('page_start','?')} |\n"
        f"| page_end | {m.get('page_end','?')} |\n"
        f"| chunk_index | {m.get('chunk_index','?')} |\n"
        f"| paper_id | {m.get('paper_id','?')} |\n\n"
    )
    return header + f"```\n{content}\n```\n"


# ─── main ───

def main():
    # Init
    bm25 = BM25Store()
    bm25.load()
    bm25.add_domain_terms()
    reranker = Reranker(passage_mode=True, fusion_enabled=False)
    scorer = HybridScorer(bm25_store=bm25, reranker=reranker)
    chunk_map = load_chunk_meta_map()
    print(f"Chunk 元数据加载: {len(chunk_map)} 条")

    # Load questions
    with open(EVAL_PATH) as f:
        questions = [json.loads(l) for l in f if l.strip()]
    answerable = [q for q in questions if q.get("should_answer")]

    # ─── 逐题计算 ───
    rows = []
    for q in answerable:
        query = q["question"]
        expected_ids = q.get("expected_chunk_ids", [])
        if not expected_ids:
            continue

        docs = scorer.retrieve(query, bm25_k=50, top_k=max(K_LIST))
        retrieved_ids = [d.metadata.get("chunk_id", "") for d in docs]

        r = {
            "id": q["id"],
            "question": query,
            "answer_type": q.get("answer_type", ""),
            "lang": detect_lang(q["id"]),
            "expected_ids": expected_ids,
            "expected_sources": q.get("expected_sources", []),
            "docs": docs,
            "retrieved_ids": retrieved_ids,
        }
        for k in K_LIST:
            r[f"strict@{k}"] = compute_strict_chunk_recall_at_k(retrieved_ids, expected_ids, k)
            r[f"window@{k}"] = compute_window_chunk_recall_at_k(docs, expected_ids, k, chunk_map)
        rows.append(r)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = os.path.join(OUTPUT_DIR, f"per_question_debug_{timestamp}.md")

    with open(output_path, "w", encoding="utf-8") as f:
        w = f.write

        w("# Per-Question Chunk Recall 诊断报告\n\n")
        w(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        w(f"**数据集**: `rag_eval_20.jsonl` ({len(answerable)} answerable questions)  \n")
        w(f"**检索策略**: `hybrid_score` (BM25 45% + Reranker 25% + Keyword 20% + Metadata 10%)  \n")
        w(f"**k 值**: {K_LIST}\n\n")
        w("---\n\n")

        # ─── 1. 逐题详情 ───
        w("# 1. 逐题详情\n\n")
        # Sort by strict@5 ascending (worst first)
        rows_sorted = sorted(rows, key=lambda r: r.get("strict@5", 0) or 0)

        for idx, r in enumerate(rows_sorted, 1):
            qid = r["id"]
            w(f"## {idx}. [{qid}] {r['question'][:120]}\n\n")
            w(f"**Type**: `{r['answer_type']}` | **Lang**: `{r['lang']}` | "
              f"**Expected chunks**: {len(r['expected_ids'])}\n\n")

            # Recall table
            w("| k | strict_recall | window_recall |\n")
            w("|---|--------------|---------------|\n")
            for k in K_LIST:
                sv = r.get(f"strict@{k}")
                wv = r.get(f"window@{k}")
                s_str = f"{sv:.4f}" if sv is not None else "N/A"
                w_str = f"{wv:.4f}" if wv is not None else "N/A"
                w(f"| {k} | {s_str} | {w_str} |\n")
            w("\n")

            # Expected sources
            if r["expected_sources"]:
                w("**Expected sources**: ")
                w(", ".join(s.get("filename_contains", "?") for s in r["expected_sources"]))
                w("\n\n")

            # Expected chunks with full content
            w(f"### Expected Chunks ({len(r['expected_ids'])})\n\n")
            for cid in r["expected_ids"]:
                w(fmt_chunk_full(cid, chunk_map))
                w("\n")

            # Retrieved top-k (use max K_LIST = 20)
            w(f"### Retrieved Top-{max(K_LIST)}\n\n")
            top_docs = r["docs"][:max(K_LIST)]
            for i, d in enumerate(top_docs, 1):
                cid = d.metadata.get("chunk_id", "")
                hit = " **[HIT]**" if cid in r["expected_ids"] else ""
                rank_info = f"**#{i}**{hit} — "
                w(rank_info + fmt_chunk_meta(cid, chunk_map) + "\n\n")
                # Full content for retrieved chunks
                info = chunk_map.get(cid)
                if info:
                    w(f"```\n{info['content'][:500]}\n```\n\n")

            # Missed chunks
            top_k_ids = set(r["retrieved_ids"][:max(K_LIST)])
            missed = [cid for cid in r["expected_ids"] if cid not in top_k_ids]
            w(f"### Missed Chunks ({len(missed)} — expected but NOT in top-{max(K_LIST)})\n\n")
            if missed:
                for cid in missed:
                    w(fmt_chunk_full(cid, chunk_map))
                    w("\n")
            else:
                w("*None — all expected chunks were retrieved.*\n\n")

            # False positives
            fp = [cid for cid in r["retrieved_ids"][:max(K_LIST)] if cid not in set(r["expected_ids"])]
            w(f"### False Positives ({len(fp)} — in top-{max(K_LIST)} but NOT expected)\n\n")
            if fp:
                for cid in fp:
                    w(fmt_chunk_full(cid, chunk_map))
                    w("\n")
            else:
                w("*None — all retrieved chunks matched expectations.*\n\n")

            w("---\n\n")

        # ─── 2. 按 answer_type 汇总 ───
        w("# 2. 按问题类型汇总\n\n")
        type_groups = defaultdict(list)
        for r in rows:
            type_groups[r["answer_type"]].append(r)

        for atype in sorted(type_groups.keys()):
            group = type_groups[atype]
            w(f"## {atype} ({len(group)} questions)\n\n")
            w("| k | avg strict_recall | avg window_recall |\n")
            w("|---|-------------------|-------------------|\n")
            for k in K_LIST:
                strict_vals = [r[f"strict@{k}"] for r in group if r.get(f"strict@{k}") is not None]
                window_vals = [r[f"window@{k}"] for r in group if r.get(f"window@{k}") is not None]
                avg_s = sum(strict_vals) / len(strict_vals) if strict_vals else 0
                avg_w = sum(window_vals) / len(window_vals) if window_vals else 0
                w(f"| {k} | {avg_s:.4f} | {avg_w:.4f} |\n")
            w("\n")

            # Per-question table for this type
            w("| ID | Lang | strict@5 | window@5 | strict@10 | window@10 |\n")
            w("|----|------|----------|----------|-----------|----------|\n")
            for r in group:
                s5 = r.get("strict@5") or 0
                w5 = r.get("window@5") or 0
                s10 = r.get("strict@10") or 0
                w10 = r.get("window@10") or 0
                w(f"| {r['id']} | {r['lang']} | {s5:.2f} | {w5:.2f} | {s10:.2f} | {w10:.2f} |\n")
            w("\n")

        # ─── 3. 按语言汇总 ───
        w("# 3. 按语言汇总 (EN vs ZH)\n\n")
        lang_groups = defaultdict(list)
        for r in rows:
            lang_groups[r["lang"]].append(r)

        for lang in ["EN", "ZH"]:
            group = lang_groups.get(lang, [])
            if not group:
                continue
            w(f"## {lang} ({len(group)} questions)\n\n")
            w("| k | avg strict_recall | avg window_recall |\n")
            w("|---|-------------------|-------------------|\n")
            for k in K_LIST:
                strict_vals = [r[f"strict@{k}"] for r in group if r.get(f"strict@{k}") is not None]
                window_vals = [r[f"window@{k}"] for r in group if r.get(f"window@{k}") is not None]
                avg_s = sum(strict_vals) / len(strict_vals) if strict_vals else 0
                avg_w = sum(window_vals) / len(window_vals) if window_vals else 0
                w(f"| {k} | {avg_s:.4f} | {avg_w:.4f} |\n")
            w("\n")

        # ─── 4. 全局汇总 ───
        w("# 4. 全局汇总 (all answerable questions)\n\n")
        w("| k | avg strict_recall | avg window_recall |\n")
        w("|---|-------------------|-------------------|\n")
        for k in K_LIST:
            strict_vals = [r[f"strict@{k}"] for r in rows if r.get(f"strict@{k}") is not None]
            window_vals = [r[f"window@{k}"] for r in rows if r.get(f"window@{k}") is not None]
            avg_s = sum(strict_vals) / len(strict_vals) if strict_vals else 0
            avg_w = sum(window_vals) / len(window_vals) if window_vals else 0
            w(f"| {k} | {avg_s:.4f} | {avg_w:.4f} |\n")
        w("\n")

        # Per-question quick table
        w("## 所有题目速览 (sorted by strict@5)\n\n")
        w("| # | ID | Type | Lang | strict@5 | window@5 | strict@10 | window@10 | strict@20 | window@20 |\n")
        w("|---|----|------|------|----------|----------|-----------|----------|-----------|----------|\n")
        for i, r in enumerate(rows_sorted, 1):
            s5 = r.get("strict@5") or 0
            w5 = r.get("window@5") or 0
            s10 = r.get("strict@10") or 0
            w10 = r.get("window@10") or 0
            s20 = r.get("strict@20") or 0
            w20 = r.get("window@20") or 0
            w(f"| {i} | {r['id']} | {r['answer_type']} | {r['lang']} | "
              f"{s5:.2f} | {w5:.2f} | {s10:.2f} | {w10:.2f} | {s20:.2f} | {w20:.2f} |\n")

    print(f"Report written to: {output_path}")


if __name__ == "__main__":
    main()
