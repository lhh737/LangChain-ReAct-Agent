"""
RAGAS 检索质量评估 — Phase 1: Context Precision / Recall / Entity Recall

用法：python evaluation/ragas_eval.py
报告：evaluation/reports/ragas_<timestamp>.md
依赖：pip install ragas
"""
import sys
import os
import json
import time
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# LangChain 0.3 去掉了 deprecated 导入路径，ragas 可能引用旧路径
import langchain  # noqa: F401

from langchain_core.documents import Document
from rag.vector_store import VectorStoreService
from rag.bm25_store import BM25Store
from rag.retrieval_strategy import HybridScorer, HybridRetriever, Reranker
from rag.rag_service import RagSummarizeService
from model.factory import chat_model, embed_model
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
from evaluation.multi_query_eval import _translate_zh_query
from pydantic import BaseModel

# ─── RAGAS 导入（版本自适应） ───
try:
    from ragas import evaluate, SingleTurnSample, EvaluationDataset
    from ragas.llms import llm_factory
    from openai import OpenAI
    RAGAS_V2 = True
except ImportError:
    RAGAS_V2 = False

try:
    from ragas.metrics import ContextPrecision, ContextRecall, ContextEntityRecall
    RAGAS_METRICS_V2 = True
except ImportError:
    from ragas.metrics import context_precision, context_recall, context_entity_recall
    RAGAS_METRICS_V2 = False

# ─── 配置 ───
EVAL_PATH = get_abs_path("evaluation/rag_eval_20.jsonl")
MULTI_CACHE_PATH = get_abs_path("evaluation/multi_query_cache.json")
ZH_TRANSLATE_CACHE_PATH = get_abs_path("evaluation/zh_translate_cache.json")
REPORT_DIR = get_abs_path("evaluation/reports")
RETRIEVAL_TOP_K = 10
MAX_SAMPLES = int(os.getenv("RAGAS_MAX_SAMPLES", "0")) or None  # None=全量；设 2 即只跑 2 题
BATCH_SIZE = int(os.getenv("RAGAS_BATCH_SIZE", "8"))             # LLM judge 并发批次
STRATEGY = os.getenv("RAGAS_STRATEGY", "all")                    # "all" / "mq_rrf" / "hybrid_rerank"
FALLBACK_STRATEGY = "hybrid_score_raw"

# ─── 初始化 ───

def init_retrievers():
    vs = VectorStoreService()
    bm25 = BM25Store()
    bm25.load()
    bm25.add_domain_terms()

    # MQ RRF 组件
    hyb_scorer = HybridScorer(
        bm25_store=bm25,
        reranker=Reranker(passage_mode=True, fusion_enabled=False),
    )

    # hybrid_rerank 组件（对齐 retrieval_eval.py）
    hybrid = HybridRetriever(
        vector_store=vs.vector_store,
        bm25_store=bm25,
    )
    reranker = Reranker()  # baseline: 无 passage，无 fusion

    return vs, bm25, hyb_scorer, hybrid, reranker


def _mq_rrf_retrieve(query, mq_plan, bm25, vs, hyb_scorer, top_k=RETRIEVAL_TOP_K):
    """复用 retrieval_eval.py 的 MQ RRF 管线（精简版）"""
    from evaluation.multi_query_eval import multi_query_retrieve

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
    rrf_scores = {}
    for sq_scores in all_subq_scores:
        ranked = sorted(sq_scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (i, _) in enumerate(ranked, 1):
            rrf_scores[i] = rrf_scores.get(i, 0) + 1.0 / (RRF_K + rank)

    # BM25 safeguard
    N = len(mq_pool)
    bm25_max = {i: max(bs[i] for bs in all_subq_bm25) for i in range(N)}
    bm25_top5 = {i for i, _ in sorted(bm25_max.items(), key=lambda x: x[1], reverse=True)[:5]}

    ranking = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
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


def _hybrid_rerank_retrieve(query, hybrid, reranker, top_k=RETRIEVAL_TOP_K):
    """RRF 粗排（50）→ Reranker 精排 → top-k（对齐 retrieval_eval.py 的 hybrid_rerank）"""
    candidates = hybrid.retrieve(query, k=50)
    return reranker.rerank(query, candidates, top_k=top_k)


def _hybrid_rerank_translate_retrieve(query, hybrid, reranker, zh_cache=None, top_k=RETRIEVAL_TOP_K):
    """LLM 自动检测语言：英文原样，中文翻译后走 hybrid_rerank 检索"""
    if zh_cache is not None:
        translated = _translate_zh_query(query, zh_cache)
    else:
        translated = query
    return _hybrid_rerank_retrieve(translated, hybrid, reranker, top_k=top_k)


def _agent_production_retrieve(query, rag_service=None, top_k=RETRIEVAL_TOP_K):
    """Agent 生产管线：直接调用 RagSummarizeService.retriever_docs()，100% 对齐实际检索路径"""
    if rag_service is None:
        return _hybrid_rerank_retrieve(query, None, None)  # fallback
    return rag_service.retriever_docs(query)[:top_k]


def _hybrid_score_translate_retrieve(query, hyb_scorer, zh_cache=None, top_k=RETRIEVAL_TOP_K):
    """LLM 检测语言 + HybridScorer 加权融合（对齐 multi_query_eval 的 tr 策略）"""
    if zh_cache is not None:
        translated = _translate_zh_query(query, zh_cache)
    else:
        translated = query
    return hyb_scorer.retrieve(translated, bm25_k=50, top_k=top_k)


# 策略注册表
STRATEGIES = {
    "agent_production": _agent_production_retrieve,
    "mq_rrf": _mq_rrf_retrieve,
    "hybrid_rerank": _hybrid_rerank_retrieve,
    "hybrid_rerank_translate": _hybrid_rerank_translate_retrieve,
    "hybrid_score_translate": _hybrid_score_translate_retrieve,
}


def build_reference(gold_facts: list[str]) -> str:
    """将 gold_facts 拼接为 RAGAS reference 字符串"""
    return "\n".join(f"- {f}" for f in gold_facts)


# ─── 主流程 ───

def _build_ragas_metrics(judge):
    """创建 RAGAS 指标列表"""
    if RAGAS_V2 and RAGAS_METRICS_V2:
        return [
            ContextPrecision(llm=judge),
            ContextRecall(llm=judge),
            ContextEntityRecall(llm=judge),
        ]
    elif RAGAS_V2:
        return [context_precision, context_recall, context_entity_recall]
    else:
        return [context_precision, context_recall, context_entity_recall]


def _run_ragas_for_strategy(name, retrieve_fn, answerable, judge, extra_args, metric_names):
    """对单个检索策略构建 samples + 跑 RAGAS evaluate，返回 (result, retrieval_info, elapsed)"""
    samples = []
    retrieval_info = []

    print(f"\n  [{name}] 检索 + 构建 samples...")
    for q in answerable:
        qid = q["id"]
        query = q["question"]
        reference = build_reference(q["gold_facts"])

        try:
            retrieved = retrieve_fn(query, **extra_args.get(name, {}))
        except Exception as e:
            logger.warning(f"[RAGAS] {name} {qid} 失败：{e}")
            retrieved = []

        contexts = [d.page_content for d in retrieved[:RETRIEVAL_TOP_K]]

        if RAGAS_V2:
            sample = SingleTurnSample(
                user_input=query,
                retrieved_contexts=contexts,
                reference=reference,
            )
        else:
            sample = {
                "question": query,
                "contexts": contexts,
                "reference": reference,
            }

        samples.append(sample)
        retrieval_info.append({
            "id": qid,
            "query": query,
            "reference": reference,
            "contexts": contexts,
            "num_contexts": len(contexts),
            "context_lengths": [len(c) for c in contexts],
        })

    print(f"  [{name}] RAGAS 评估 {len(samples)} samples...")
    t0 = time.time()

    metrics = _build_ragas_metrics(judge)

    if RAGAS_V2:
        dataset = EvaluationDataset(samples)
        result = evaluate(dataset, metrics=metrics, llm=judge, batch_size=BATCH_SIZE)
    else:
        from datasets import Dataset
        ds = Dataset.from_dict({
            "question": [s["question"] for s in samples],
            "contexts": [s["contexts"] for s in samples],
            "reference": [s["reference"] for s in samples],
        })
        result = evaluate(ds, metrics=metrics, batch_size=BATCH_SIZE)

    elapsed = time.time() - t0
    print(f"  [{name}] 完成，耗时 {elapsed:.1f}s")
    return result, retrieval_info, elapsed


# ─── 逐 chunk LLM 判定 + debug 输出 ───

class ChunkVerdict(BaseModel):
    index: int
    relevant: bool
    reason: str


class ChunkJudgments(BaseModel):
    verdicts: list[ChunkVerdict]


def _judge_chunks_batch(judge, query, reference, contexts):
    """一次 LLM 调用判定所有 chunk 与 reference 的相关性"""
    if not contexts:
        return []

    chunks_text = "\n\n".join(
        f"[Chunk {i}]\n{ctx[:1500]}"
        for i, ctx in enumerate(contexts)
    )

    prompt = f"""You are evaluating retrieval quality. Given a user query and reference facts, judge whether each retrieved chunk is relevant to the reference.

## Query
{query}

## Reference Facts
{reference}

## Retrieved Chunks
{chunks_text}

For each chunk, determine if it contains information that helps answer the query based on the reference facts. Set relevant=true only if the chunk directly relates to at least one reference fact. Provide a brief reason in Chinese."""

    try:
        result = judge.generate(prompt=prompt, response_model=ChunkJudgments)
        return result.verdicts
    except Exception as e:
        logger.warning(f"逐 chunk 判定失败：{e}")
        return []


def _write_debug_file(strategy_name, retrieval_info, judge, filepath):
    """输出 debug.txt：chunk 原文 + LLM 逐 chunk 判定"""
    with open(filepath, "w", encoding="utf-8") as f:
        w = f.write
        w(f"RAGAS Debug — 策略: {strategy_name}\n")
        w(f"=" * 80 + "\n\n")

        for idx, info in enumerate(retrieval_info):
            qid = info["id"]
            query = info["query"]
            reference = info["reference"]
            contexts = info["contexts"]

            w(f"## [{idx+1}] {qid}\n\n")
            w(f"**Query**: {query}\n\n")
            w(f"**Reference**:\n{reference}\n\n")

            # LLM 逐 chunk 判定
            print(f"  [debug:{strategy_name}] 判定 {qid} 的 {len(contexts)} chunks...")
            verdicts = _judge_chunks_batch(judge, query, reference, contexts)

            verdict_map = {}
            if verdicts:
                for v in verdicts:
                    verdict_map[v.index] = v

            relevant_count = 0
            w(f"**Chunks ({len(contexts)})**:\n\n")
            for i, ctx in enumerate(contexts):
                v = verdict_map.get(i)
                if v is not None:
                    tag = "✓ RELEVANT" if v.relevant else "✗ NOT_RELEVANT"
                    if v.relevant:
                        relevant_count += 1
                    reason = v.reason
                else:
                    tag = "? JUDGE_FAILED"
                    reason = "N/A"

                w(f"--- Chunk #{i} [{tag}] ---\n")
                w(f"Reason: {reason}\n")
                w(f"{ctx}\n\n")

            precision_k = relevant_count / len(contexts) if contexts else 0
            w(f"**LLM判定汇总**: {relevant_count}/{len(contexts)} relevant → precision={precision_k:.4f}\n\n")

    print(f"  debug → {filepath}")



def run_ragas_eval():
    os.makedirs(REPORT_DIR, exist_ok=True)

    # 加载数据
    with open(EVAL_PATH) as f:
        all_questions = [json.loads(l) for l in f if l.strip()]
    with open(MULTI_CACHE_PATH) as f:
        multi_cache = json.load(f)

    answerable = [q for q in all_questions if q.get("should_answer") and q.get("gold_facts")]
    if MAX_SAMPLES:
        answerable = answerable[:MAX_SAMPLES]
    print(f"加载 {len(all_questions)} 题：可答（有 gold_facts）{len(answerable)}"
          + (f"（MAX_SAMPLES={MAX_SAMPLES}）" if MAX_SAMPLES else ""))

    # 初始化检索
    vs, bm25, hyb_scorer, hybrid, reranker = init_retrievers()

    # 初始化生产 RAG 管线
    rag_service = RagSummarizeService()
    print(f"生产管线初始化完成")

    # 加载中→英翻译缓存
    zh_cache = {}
    if os.path.exists(ZH_TRANSLATE_CACHE_PATH):
        with open(ZH_TRANSLATE_CACHE_PATH) as f:
            zh_cache = json.load(f)
    print(f"加载中→英翻译缓存：{len(zh_cache)} 条")

    # 初始化 RAGAS judge（LLM）
    if RAGAS_V2:
        client = OpenAI(
            api_key=os.getenv("SILICONFLOW_API_KEY", ""),
            base_url="https://api.siliconflow.cn/v1",
        )
        judge = llm_factory("deepseek-ai/DeepSeek-V4-Flash", client=client)
    else:
        judge = None

    metric_names = ["context_precision", "context_recall", "context_entity_recall"]

    # 选择策略
    active_names = list(STRATEGIES.keys()) if STRATEGY == "all" else [STRATEGY]

    # 为不同策略准备参数
    extra_args = {
        "agent_production": {"rag_service": rag_service},
        "mq_rrf": {},
        "hybrid_rerank": {"hybrid": hybrid, "reranker": reranker},
        "hybrid_rerank_translate": {"hybrid": hybrid, "reranker": reranker, "zh_cache": zh_cache},
        "hybrid_score_translate": {"hyb_scorer": hyb_scorer, "zh_cache": zh_cache},
    }
    # mq_rrf 需要额外注入 bm25/vs/hyb_scorer/mq_plan（逐题动态）
    # 用闭包包装
    def _make_mq_rrf_fn():
        def fn(query, **_kw):
            # 找到当前 query 对应的 multi_cache entry
            _qid = None
            for _q in answerable:
                if _q["question"] == query:
                    _qid = _q["id"]
                    break
            mq_plan = multi_cache.get(_qid, {"subqueries": [{"entity": "fallback", "query": query}]})
            try:
                return _mq_rrf_retrieve(query, mq_plan, bm25, vs, hyb_scorer)
            except Exception:
                return hyb_scorer.retrieve(query, bm25_k=50, top_k=RETRIEVAL_TOP_K)
        return fn

    def _make_hybrid_rerank_fn():
        def fn(query, hybrid=hybrid, reranker=reranker, **_kw):
            return _hybrid_rerank_retrieve(query, hybrid, reranker)
        return fn

    def _make_hybrid_rerank_translate_fn():
        def fn(query, hybrid=hybrid, reranker=reranker, zh_cache=zh_cache, **_kw):
            return _hybrid_rerank_translate_retrieve(query, hybrid, reranker, zh_cache)
        return fn

    def _make_hybrid_score_translate_fn():
        def fn(query, hyb_scorer=hyb_scorer, zh_cache=zh_cache, **_kw):
            return _hybrid_score_translate_retrieve(query, hyb_scorer, zh_cache)
        return fn

    def _make_agent_production_fn():
        def fn(query, rag_service=rag_service, **_kw):
            return _agent_production_retrieve(query, rag_service)
        return fn

    strategy_fns = {
        "agent_production": _make_agent_production_fn(),
        "mq_rrf": _make_mq_rrf_fn(),
        "hybrid_rerank": _make_hybrid_rerank_fn(),
        "hybrid_rerank_translate": _make_hybrid_rerank_translate_fn(),
        "hybrid_score_translate": _make_hybrid_score_translate_fn(),
    }

    # 逐策略评估
    all_results: dict[str, dict] = {}
    all_infos: dict[str, list] = {}
    all_elapsed: dict[str, float] = {}

    for name in active_names:
        if name not in STRATEGIES:
            print(f"未知策略 {name}，跳过")
            continue
        result, info, elapsed = _run_ragas_for_strategy(
            name, strategy_fns[name], answerable, judge, extra_args, metric_names,
        )
        all_results[name] = result
        all_infos[name] = info
        all_elapsed[name] = elapsed

        # 输出 debug.txt（chunk 原文 + LLM 逐 chunk 判定）
        ts = datetime.now().strftime("%Y%m%d_%H%M")
        debug_path = os.path.join(REPORT_DIR, f"ragas_debug_{ts}_{name}.txt")
        _write_debug_file(name, info, judge, debug_path)

    # ── 生成报告 ──
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    report_path = os.path.join(REPORT_DIR, f"ragas_{ts}.md")
    total_elapsed = sum(all_elapsed.values())

    with open(report_path, "w", encoding="utf-8") as f:
        w = f.write
        w("# RAGAS 检索质量评估报告 (Phase 1)\n\n")
        w(f"**评估时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        w(f"**样本数**: {len(answerable)}（仅可答题） | **检索策略**: {', '.join(active_names)} → top-{RETRIEVAL_TOP_K}  \n")
        w(f"**LLM Judge**: DeepSeek-V4-Flash (temperature=0.0)  \n")
        w(f"**总耗时**: {total_elapsed:.1f}s  \n\n")

        # ── 策略对比总览 ──
        w("## 策略对比总览\n\n")
        if len(active_names) > 1:
            w("| 指标 | " + " | ".join(active_names) + " |\n")
            w("|------|" + "|".join(["------"] * len(active_names)) + "|\n")
            for m in metric_names:
                vals = []
                for name in active_names:
                    raw = [v for v in all_results[name][m] if v is not None]
                    avg = sum(raw) / len(raw) if raw else float("nan")
                    vals.append(f"{avg:.4f}")
                w(f"| {m} | " + " | ".join(vals) + " |\n")
            w("\n")
        else:
            name = active_names[0]
            result = all_results[name]
            w("| 指标 | 均值 |\n")
            w("|------|------|\n")
            for m in metric_names:
                vals = [v for v in result[m] if v is not None]
                avg = sum(vals) / len(vals) if vals else float("nan")
                w(f"| {m} | {avg:.4f} |\n")
            w("\n")

        w("## 指标说明\n\n")
        w("- **Context Precision**: 检索到的 contexts 中与 reference 相关的比例（越高越好，衡量精度）\n")
        w("- **Context Recall**: reference 中需要的信息在 contexts 中能找回的比例（越高越好，衡量召回）\n")
        w("- **Context Entity Recall**: reference 中提到的实体在 contexts 中出现的比例（越高越好，衡量实体覆盖）\n\n")

        # ── 逐题对比 ──
        w("## 逐题对比\n\n")
        if len(active_names) > 1:
            # 多策略：每个指标一个小表
            for m in metric_names:
                w(f"### {m}\n\n")
                header = "| ID | " + " | ".join(active_names) + " |\n"
                sep = "|------|" + "|".join(["------"] * len(active_names)) + "|\n"
                w(header + sep)
                for i, info in enumerate(all_infos[active_names[0]]):
                    row = f"| {info['id']} |"
                    for name in active_names:
                        v = all_results[name][m][i]
                        row += f" {v:.4f} |" if v is not None else " N/A |"
                    w(row + "\n")
                w("\n")
        else:
            name = active_names[0]
            result = all_results[name]
            w("| ID | Question | Context Precision | Context Recall | Entity Recall |\n")
            w("|------|----------|-------------------|---------------|-------------|\n")
            for i, info in enumerate(all_infos[name]):
                row = f"| {info['id']} | {info['query'][:80]}... |"
                for m in metric_names:
                    v = result[m][i]
                    row += f" {v:.4f} |" if v is not None else " N/A |"
                w(row + "\n")
            w("\n")

        # ── 各策略样本详情 ──
        for name in active_names:
            result = all_results[name]
            info_list = all_infos[name]
            w(f"## {name} 样本详情\n\n")
            for i, info in enumerate(info_list):
                w(f"### {info['id']}\n\n")
                w(f"**Query**: {info['query']}  \n")
                w(f"**Contexts ({info['num_contexts']})**:  \n")
                for j, cl in enumerate(info["context_lengths"], 1):
                    cp_val = result["context_precision"][i]
                    cr_val = result["context_recall"][i]
                    w(f"  - chunk#{j}: {cl} chars | "
                      f"precision={cp_val:.4f} | recall={cr_val:.4f}  \n")
                w("\n")

    print(f"报告 → {report_path}")


if __name__ == "__main__":
    run_ragas_eval()

def main(argv=None) -> int:
    """CLI 入口"""
    run_ragas_eval()
    return 0
