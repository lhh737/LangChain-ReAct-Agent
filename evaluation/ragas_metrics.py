"""基于 RAGAS 的评估指标封装（简化版，本地计算）"""

from langchain_core.documents import Document
from utils.logger_handler import logger


class RagasEvaluator:
    """学术 RAG 评估器：计算 Faithfulness、Context Precision 等指标"""

    def __init__(self):
        self.results: list[dict] = []

    def evaluate_single(
        self,
        question: str,
        answer: str,
        contexts: list[str],
        ground_truth: str | None = None,
    ) -> dict:
        """对单个 QA 对计算所有指标"""
        metrics = {}

        # 检索命中率：上下文中是否包含关键术语
        if ground_truth:
            metrics["retrieval_hit_rate"] = self._compute_hit_rate(answer, contexts)

        # Context Precision 简化：有效上下文占比
        metrics["context_precision"] = self._compute_context_precision(question, contexts)

        # Faithfulness 简化：回答中声明是否能在上下文中找到支撑
        metrics["faithfulness"] = self._compute_faithfulness(answer, contexts)

        # Response Relevancy 简化：回答是否与问题相关
        metrics["answer_relevancy"] = self._compute_relevancy(question, answer)

        return metrics

    def _compute_hit_rate(self, answer: str, contexts: list[str]) -> float:
        """检查回答中的关键信息是否源于上下文"""
        if not contexts:
            return 0.0
        context_text = " ".join(contexts).lower()
        # 取回答中引用的关键词
        answer_keywords = self._extract_key_terms(answer)
        if not answer_keywords:
            return 0.5
        hits = sum(1 for kw in answer_keywords if kw.lower() in context_text)
        return hits / len(answer_keywords)

    def _compute_context_precision(self, question: str, contexts: list[str]) -> float:
        """上下文精确度：多少上下文与问题相关"""
        if not contexts:
            return 0.0
        question_terms = set(self._extract_key_terms(question))
        scores = []
        for ctx in contexts:
            ctx_terms = set(self._extract_key_terms(ctx))
            if question_terms:
                overlap = len(question_terms & ctx_terms) / len(question_terms)
                scores.append(min(overlap, 1.0))
            else:
                scores.append(0.0)
        return sum(scores) / len(scores) if scores else 0.0

    def _compute_faithfulness(self, answer: str, contexts: list[str]) -> float:
        """忠实度：回答中的声明是否有上下文支撑"""
        if not contexts or not answer:
            return 0.0
        context_text = " ".join(contexts).lower()
        answer_sentences = [s.strip() for s in answer.replace("。", ".").split(".") if s.strip()]
        if not answer_sentences:
            return 0.0
        supported = 0
        for sentence in answer_sentences:
            terms = self._extract_key_terms(sentence)
            if not terms:
                continue
            if any(t.lower() in context_text for t in terms[:3]):
                supported += 1
        return supported / len(answer_sentences)

    def _compute_relevancy(self, question: str, answer: str) -> float:
        """回答相关性：回答是否围绕提问展开"""
        if not answer or not question:
            return 0.0
        q_terms = set(self._extract_key_terms(question))
        a_terms = set(self._extract_key_terms(answer))
        if not q_terms:
            return 0.5
        overlap = len(q_terms & a_terms)
        return min(overlap / len(q_terms), 1.0)

    def _compute_citation_validity(self, answer: str, retrieved_docs: list) -> float:
        """引用合法性：从 academic_search 检索结果推断有效 [N] 范围，检查回答中引用是否合法"""
        import re

        # 有效引用范围 = 检索返回的文档数
        max_valid = len(retrieved_docs)

        if max_valid == 0:
            return 1.0  # 无检索结果，无引用需求

        cited = [int(m) for m in re.findall(r"\[(\d+)\]", answer)]
        if not cited:
            # 检索有结果但回答不引用 → 扣分
            return 0.0

        valid = sum(1 for n in cited if 1 <= n <= max_valid)
        return valid / len(cited)

    def _extract_key_terms(self, text: str) -> list[str]:
        """提取文本中的关键术语（中英文混合）"""
        import re
        # 英文术语：2个以上大写字母开头的词或驼峰词
        en_terms = re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b", text)
        # 中文术语：2-6 个连续汉字
        cn_terms = re.findall(r"[一-鿿]{2,6}", text)
        return en_terms + cn_terms


if __name__ == "__main__":
    evaluator = RagasEvaluator()
    result = evaluator.evaluate_single(
        question="深度学习的优化方法有哪些？",
        answer="深度学习主要使用 SGD、Adam 等优化器。根据某论文，Adam 结合了动量和自适应学习率。",
        contexts=["Adam optimizer combines momentum and adaptive learning rate.", "SGD is a basic optimizer."],
        ground_truth="SGD, Adam, RMSprop",
    )
    for k, v in result.items():
        print(f"{k}: {v:.2f}")
