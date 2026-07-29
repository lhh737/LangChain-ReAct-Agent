"""科研论文问答质量评估器：RAG 直连 + Agent 端到端 双层评估"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import time
import json
from utils.path_tool import get_abs_path
from rag.rag_service import RagSummarizeService
from agent.react_agent import ReactAgent
from evaluation.ragas_metrics import RagasEvaluator

try:
    from ragas import evaluate, SingleTurnSample, EvaluationDataset
    from ragas.llms import llm_factory
    from ragas.metrics import ContextPrecision, ContextRecall
    from openai import OpenAI
    RAGAS_V2 = True
    HAS_RAGAS = True
except ImportError:
    try:
        from ragas.metrics import context_precision, context_recall  # v1 回退
        RAGAS_V2 = False
        HAS_RAGAS = True
    except ImportError:
        HAS_RAGAS = False
        RAGAS_V2 = False


class ProgramQAEvaluator:
    """端到端问答质量评估器，支持 RAG 直连和 Agent 全链路两种评估模式"""

    def __init__(self):
        self.rag_service = RagSummarizeService()
        self.ragas = RagasEvaluator()
        self.test_questions = self._load_test_questions()
        self._ragas_judge = None
        if HAS_RAGAS:
            client = OpenAI(
                api_key=os.getenv("SILICONFLOW_API_KEY", ""),
                base_url="https://api.siliconflow.cn/v1",
            )
            self._ragas_judge = llm_factory("deepseek-ai/DeepSeek-V4-Flash", client=client)

    def _load_test_questions(self) -> list[dict]:
        import json
        path = get_abs_path("evaluation/rag_eval_20.jsonl")
        questions = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                q = json.loads(line)
                if not q.get("should_answer", True):
                    continue
                qid = q.get("id", "")
                if qid in ("cross_002_en", "cross_002_zh"):
                    continue
                questions.append({
                    "id": qid,
                    "category": q.get("answer_type", "other"),
                    "question": q["question"],
                    "gold_facts": q.get("gold_facts", []),
                })
        return questions

    # ────────── RAG 直连评估（保留）──────────

    def run_rag_eval(self) -> list[dict]:
        """RAG 直连：rag_summarize() → 计算 Faithfulness / RAGAS Precision/Recall 等"""
        results = []
        total = len(self.test_questions)
        # 批量 RAGAS 评估所需的缓存
        ragas_samples: list[tuple[int, str, str, list[str]]] = []  # (idx, query, reference, contexts)

        for i, q in enumerate(self.test_questions):
            print(f"\n[RAG直连 {i+1}/{total}] {q['question'][:60]}...")

            start = time.time()
            try:
                answer = self.rag_service.rag_summarize(q["question"])
            except Exception as e:
                answer = f"[ERROR] {e}"
            elapsed = time.time() - start

            try:
                docs = self.rag_service.retriever_docs(q["question"])
                contexts = [d.page_content for d in docs]
            except Exception:
                docs, contexts = [], []

            metrics = self.ragas.evaluate_single(
                question=q["question"],
                answer=answer,
                contexts=contexts,
            )
            metrics["response_time"] = round(elapsed, 2)
            metrics["num_contexts"] = len(contexts)
            metrics["citation_accuracy"] = self._check_citation_accuracy(answer, docs)

            results.append({
                "id": q["id"],
                "category": q["category"],
                "question": q["question"],
                "answer_preview": answer[:300],
                "metrics": metrics,
            })

            # 收集 RAGAS 评估样本
            gold_facts = q.get("gold_facts", [])
            if gold_facts and contexts:
                reference = "\n".join(f"- {f}" for f in gold_facts)
                ragas_samples.append((i, q["question"], reference, contexts))

            print(f"  faithfulness={metrics.get('faithfulness', 0):.2f}, "
                  f"precision={metrics.get('context_precision', 0):.2f}, "
                  f"time={elapsed:.1f}s")

        # ── 批量 RAGAS LLM Judge 评估 ──
        if ragas_samples and self._ragas_judge is not None:
            print(f"\n[RAGAS批量评估] {len(ragas_samples)} 题，LLM Judge...")
            try:
                samples = []
                for idx, query, reference, contexts in ragas_samples:
                    if RAGAS_V2:
                        samples.append(SingleTurnSample(
                            user_input=query,
                            retrieved_contexts=contexts,
                            reference=reference,
                        ))
                    else:
                        samples.append({
                            "question": query,
                            "contexts": contexts,
                            "reference": reference,
                        })

                if RAGAS_V2:
                    dataset = EvaluationDataset(samples)
                    ragas_result = evaluate(
                        dataset,
                        metrics=[ContextPrecision(llm=self._ragas_judge),
                                 ContextRecall(llm=self._ragas_judge)],
                        llm=self._ragas_judge,
                        batch_size=8,
                    )
                else:
                    from datasets import Dataset
                    ds = Dataset.from_dict({
                        "question": [s["question"] for s in samples],
                        "contexts": [s["contexts"] for s in samples],
                        "reference": [s["reference"] for s in samples],
                    })
                    ragas_result = evaluate(
                        ds,
                        metrics=[context_precision, context_recall],
                        batch_size=8,
                    )

                # 合并回 results
                for j, (idx, _, _, _) in enumerate(ragas_samples):
                    cp = ragas_result["context_precision"][j]
                    cr = ragas_result["context_recall"][j]
                    results[idx]["metrics"]["context_precision"] = cp if cp is not None else 0.0
                    results[idx]["metrics"]["context_recall"] = cr if cr is not None else 0.0
                    print(f"  {results[idx]['id']}: cp={cp:.4f} cr={cr:.4f}")
            except Exception as e:
                print(f"  RAGAS 批量评估失败：{e}")

        return results

    def _check_citation_accuracy(self, answer: str, docs: list) -> float:
        """检查回答中引用的文档标题是否能在检索上下文中找到"""
        if not docs or not answer:
            return 0.0
        titles_in_context = set()
        for d in docs:
            title = d.metadata.get("paper_title", "")
            if title:
                titles_in_context.add(title.lower())

        cited_count = 0
        valid_count = 0
        for d in docs:
            title = d.metadata.get("paper_title", "")
            if title and title.lower() in answer.lower():
                cited_count += 1
                if title.lower() in titles_in_context:
                    valid_count += 1

        if cited_count == 0:
            return 1.0
        return valid_count / cited_count

    # ────────── Agent 端到端评估（新增）──────────

    def run_agent_eval(self) -> list[dict]:
        """Agent 端到端：ReactAgent.execute_stream() → 收集最终回答 → 计算指标"""
        results = []
        total = len(self.test_questions)
        agent = ReactAgent()

        for i, q in enumerate(self.test_questions, 1):
            print(f"\n[Agent端到端 {i}/{total}] {q['question'][:60]}...")

            start = time.time()
            full_answer = ""
            tool_call_count = 0
            try:
                # 收集完整流式输出
                for chunk in agent.execute_stream(q["question"]):
                    full_answer += chunk
                # 从 agent 内部状态统计工具调用次数（通过 result 属性不可直接获取）
                # 改为在流式结束后直接用 agent._get_valid_citation_max 推断
            except Exception as e:
                full_answer = f"[ERROR] {e}"
            elapsed = time.time() - start

            # 获取检索上下文
            try:
                docs = self.rag_service.retriever_docs(q["question"])
                contexts = [d.page_content for d in docs]
            except Exception:
                contexts = []

            metrics = self.ragas.evaluate_single(
                question=q["question"],
                answer=full_answer,
                contexts=contexts,
            )

            # Agent 专属指标
            try:
                docs_agent = self.rag_service.retriever_docs(q["question"])
                metrics["citation_validity"] = self.ragas._compute_citation_validity(
                    full_answer, docs_agent
                )
            except Exception:
                metrics["citation_validity"] = 0.0

            metrics["response_time"] = round(elapsed, 2)
            metrics["num_contexts"] = len(contexts)
            metrics["answer_length"] = len(full_answer)

            results.append({
                "id": q["id"],
                "category": q["category"],
                "question": q["question"],
                "answer_preview": full_answer[:300],
                "metrics": metrics,
            })

            print(f"  faithfulness={metrics.get('faithfulness', 0):.2f}, "
                  f"citation_validity={metrics.get('citation_validity', 0):.2f}, "
                  f"time={elapsed:.1f}s")

        return results

    # ────────── 报告生成（通用）──────────

    def generate_report(self, results: list[dict], mode: str = "rag") -> str:
        """生成评估报告（Markdown），mode: 'rag' | 'agent'"""
        from datetime import datetime

        title = {
            "rag": "# 科研论文智能问答 — RAG 直连评估报告",
            "agent": "# 科研论文智能问答 — Agent 端到端评估报告",
        }

        lines = [title.get(mode, "# 评估报告"), ""]
        lines.append(f"评估时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"测试问题数：{len(results)}")
        lines.append("")

        # 按类别汇总
        lines.append("## 分类汇总")
        header = "| 类别 | 数量 | Faithfulness | Context Precision | Context Recall | Response Time |"
        if mode == "agent":
            header += " Citation Validity |"
        lines.append(header)
        lines.append("|------|------|-------------|------------------|---------------|---------------|" +
                      ("--------------|" if mode == "agent" else ""))

        categories = {}
        for r in results:
            cat = r["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r)

        for cat, items in categories.items():
            avg_f = sum(r["metrics"].get("faithfulness", 0) for r in items) / len(items)
            avg_p = sum(r["metrics"].get("context_precision", 0) for r in items) / len(items)
            avg_r = sum(r["metrics"].get("context_recall", 0) for r in items) / len(items)
            avg_t = sum(r["metrics"].get("response_time", 0) for r in items) / len(items)
            row = f"| {cat} | {len(items)} | {avg_f:.2f} | {avg_p:.2f} | {avg_r:.2f} | {avg_t:.1f}s |"
            if mode == "agent":
                avg_cv = sum(r["metrics"].get("citation_validity", 0) for r in items) / len(items)
                row += f" {avg_cv:.2f} |"
            lines.append(row)

        lines.append("")

        # 总体指标
        lines.append("## 总体指标")
        all_metrics = [
            "faithfulness", "context_precision", "context_recall", "response_time",
        ]
        if mode == "agent":
            all_metrics.append("citation_validity")

        for key in all_metrics:
            vals = [r["metrics"].get(key) for r in results if r["metrics"].get(key) is not None]
            if vals:
                avg = sum(vals) / len(vals)
                lines.append(f"- **{key}**: {avg:.3f}")

        lines.append("")
        lines.append("## 逐题详情")
        for r in results:
            lines.append(f"### {r['id']} [{r['category']}]")
            lines.append(f"**Q**: {r['question']}")
            lines.append(f"**A**: {r['answer_preview']}...")
            lines.append(f"**Metrics**: {r['metrics']}")
            lines.append("")

        report = "\n".join(lines)

        output_dir = get_abs_path("evaluation/reports")
        os.makedirs(output_dir, exist_ok=True)
        report_path = os.path.join(
            output_dir,
            f"eval_{mode}_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
        )
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)

        return report


if __name__ == "__main__":
    evaluator = ProgramQAEvaluator()
    print("=" * 50, "RAG 直连评估", "=" * 50)
    results_rag = evaluator.run_rag_eval()
    print("\n" + evaluator.generate_report(results_rag, mode="rag"))

    print("\n" + "=" * 50, "Agent 端到端评估", "=" * 50)
    results_agent = evaluator.run_agent_eval()
    print("\n" + evaluator.generate_report(results_agent, mode="agent"))

def main_rag(argv=None) -> int:
    """RAG 直连评估"""
    evaluator = ProgramQAEvaluator()
    results = evaluator.run_rag_eval()
    print(evaluator.generate_report(results, mode="rag"))
    return 0


def main_agent(argv=None) -> int:
    """Agent 端到端评估"""
    evaluator = ProgramQAEvaluator()
    results = evaluator.run_agent_eval()
    print(evaluator.generate_report(results, mode="agent"))
    return 0
