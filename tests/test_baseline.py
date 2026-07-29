"""P1 重构基线测试 —— 验证当前行为，重构后回归对比"""
import json
import os
import re
import sys
import threading
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ═══════════════════════════════════════════════════════════════════
# B1: 意图路由协议
# ═══════════════════════════════════════════════════════════════════

class TestIntentRouter(unittest.TestCase):
    """当前关键词兜底路径的基线行为"""

    @classmethod
    def setUpClass(cls):
        from agent.intent_router import IntentRouter
        cls.router = IntentRouter()

    def test_qa_queries(self):
        qa_queries = [
            "Transformer 模型的核心机制是什么？",
            "ELSA3D 解决了计算机视觉领域的什么问题？",
            "PoisonedRAG 的攻击方法是什么",
        ]
        for q in qa_queries:
            with self.subTest(query=q):
                result = self.router._keyword_classify(q)
                self.assertEqual(result.value, "qa", f"query={q}")

    def test_compare_queries(self):
        queries = [
            "BERT 和 GPT 在架构上有哪些主要区别？",
            "对比 FlippedRAG 和传统 RAG 在安全性上的差异",
            "比较综述方法和元分析方法的优劣",
        ]
        for q in queries:
            with self.subTest(query=q):
                result = self.router._keyword_classify(q)
                self.assertEqual(result.value, "compare", f"query={q}")

    def test_review_queries(self):
        queries = [
            "LLM 安全领域的攻击与防御研究现状综述",
            "NLP 领域预训练语言模型研究进展",
        ]
        for q in queries:
            with self.subTest(query=q):
                result = self.router._keyword_classify(q)
                self.assertEqual(result.value, "review", f"query={q}")

    def test_known_false_positives_baseline(self):
        """高置信正则已修正误判，关键词兜底保留旧行为作为 LLM 不可达时的后备。"""
        # 高置信正则不触发，LLM 不可达时回退关键词 → 仍为 review（已知限制）
        result = self.router._keyword_classify("这篇论文 review 了什么内容")
        self.assertEqual(result.value, "review")
        # diff 仍触发 compare 关键词（高置信正则已移除 diff）
        result = self.router._keyword_classify("diffusion model 的原理是什么")
        self.assertEqual(result.value, "compare")
        """记录当前已知误判，重构后需修正"""
        # "这篇论文 review 了什么内容" → 当前误判为 review（应为 qa）
        result = self.router._keyword_classify("这篇论文 review 了什么内容")
        self.assertEqual(result.value, "review",
                         "基线: 当前误判为 review, P1-F 修正后应变为 qa")

        # "diffusion model 的原理是什么" → 当前误判为 compare（应为 qa）
        result = self.router._keyword_classify("diffusion model 的原理是什么")
        self.assertEqual(result.value, "compare",
                         "基线: 当前误判为 compare, P1-F 修正后应变为 qa")

    def test_classify_fallback_on_no_api(self):
        result = self.router.classify("hello")
        self.assertIn(result.value, ("qa", "compare", "review"))


# ═══════════════════════════════════════════════════════════════════
# B2: 流式事件协议
# ═══════════════════════════════════════════════════════════════════

class TestStreamEventProtocol(unittest.TestCase):

    def test_event_type_constants(self):
        import ast
        with open("agent/react_agent.py") as f:
            tree = ast.parse(f.read())
        types_found = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Yield) and isinstance(node.value, ast.Dict):
                for k, v in zip(node.value.keys, node.value.values):
                    if isinstance(k, ast.Constant) and k.value == "type":
                        if isinstance(v, ast.Constant):
                            types_found.add(v.value)
        expected = {"intent", "system", "text", "tool", "references"}
        self.assertEqual(types_found, expected)

    def test_tool_names_in_frontend(self):
        import ast
        with open("agent/react_agent.py") as f:
            tree = ast.parse(f.read())
        with open("app_pages/chat_page.py") as f:
            chat_source = f.read()
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Yield) and isinstance(node.value, ast.Dict):
                type_val = name_val = None
                for k, v in zip(node.value.keys, node.value.values):
                    if isinstance(k, ast.Constant):
                        if k.value == "type" and isinstance(v, ast.Constant):
                            type_val = v.value
                        if k.value == "name" and isinstance(v, ast.Constant):
                            name_val = v.value
                if type_val == "tool" and name_val:
                    names.add(name_val)
        for name in names:
            self.assertIn(f'"{name}"', chat_source,
                          f"Tool '{name}' not in chat_page TOOL_ICONS")


# ═══════════════════════════════════════════════════════════════════
# B3: 工具预算边界
# ═══════════════════════════════════════════════════════════════════

class TestBudgetBoundary(unittest.TestCase):
    """AgentExecutionPolicy.try_consume 的门控行为"""

    def test_budget_exhausted_at_16(self):
        from agent.execution_policy import AgentExecutionPolicy
        policy = AgentExecutionPolicy(max_tool_calls=15)
        for i in range(15):
            self.assertTrue(policy.try_consume(), f"call {i+1}")
        self.assertFalse(policy.try_consume(), "call 16 should be blocked")

    def test_remaining_and_consumed(self):
        from agent.execution_policy import AgentExecutionPolicy
        policy = AgentExecutionPolicy(max_tool_calls=5)
        self.assertEqual(policy.remaining, 5)
        self.assertEqual(policy.consumed, 0)
        policy.try_consume()
        self.assertEqual(policy.remaining, 4)
        self.assertEqual(policy.consumed, 1)


# ═══════════════════════════════════════════════════════════════════
# B4: 引用校验
# ═══════════════════════════════════════════════════════════════════

class TestCitationVerification(unittest.TestCase):

    @staticmethod
    def verify(answer, num_docs):
        cited = set(int(m) for m in re.findall(r"\[(\d+)\]", answer))
        invalid = sorted(n for n in cited if n < 1 or n > num_docs)
        if invalid:
            return "invalid"
        if num_docs > 0 and not cited:
            return "zero_citation"
        if any(re.search(pat, answer) for pat in
               [r"\[N\]", r"\[n\]", r"\[数字\]", r"\[编号\]", r"\[\?\]"]):
            return "placeholder"
        return "ok"

    def test_valid_citations(self):
        self.assertEqual(self.verify("根据[1]研究，[2]表明...", 3), "ok")
        self.assertEqual(self.verify("根据[1][2][3]", 3), "ok")

    def test_invalid_citation(self):
        self.assertEqual(self.verify("根据[1]研究，详见[5]", 3), "invalid")
        self.assertEqual(self.verify("根据[1]", 0), "invalid")

    def test_zero_citation(self):
        self.assertEqual(self.verify("Transformer 架构。", 3), "zero_citation")
        self.assertEqual(self.verify("", 3), "zero_citation")

    def test_placeholder_shadowed_by_zero_citation(self):
        """已知: 占位符被零引用检测短路"""
        self.assertEqual(self.verify("根据[N]研究...", 3), "zero_citation")
        self.assertEqual(self.verify("请参阅[?][编号]", 3), "zero_citation")


# ═══════════════════════════════════════════════════════════════════
# B5: COMPARE chunk 均衡分配
# ═══════════════════════════════════════════════════════════════════

class TestChunkBalance(unittest.TestCase):

    @staticmethod
    def balance(chunks, counts, max_total, min_per, max_per):
        if len(chunks) <= max_total:
            return chunks
        subject_keys = list(counts.keys())
        groups = {k: [] for k in subject_keys}
        unassigned = []
        for doc in chunks:
            title = (doc.get("paper_title", "") or "").lower()
            content = doc.get("content", "").lower()
            matched = None
            for subj in subject_keys:
                subj_lower = subj.lower()
                if subj_lower in title:
                    matched = subj; break
                if subj_lower in content:
                    matched = subj; break
            if matched:
                groups[matched].append(doc)
            else:
                unassigned.append(doc)
        result = []; remaining = max_total
        for subj in subject_keys:
            take = min(min_per, len(groups[subj]), remaining)
            result.extend(groups[subj][:take]); remaining -= take
        for subj in subject_keys:
            if remaining <= 0: break
            already = min(min_per, len(groups[subj]))
            extra = min(max_per - already, len(groups[subj]) - already, remaining)
            if extra > 0:
                result.extend(groups[subj][already:already + extra]); remaining -= extra
        if remaining > 0 and unassigned:
            result.extend(unassigned[:remaining])
        return result

    def test_small_no_truncate(self):
        chunks = [{"paper_title": "BERT Paper", "content": "x"}]
        result = self.balance(chunks, {"BERT": 1}, 10, 2, 4)
        self.assertEqual(len(result), 1)

    def test_balanced_two_subjects(self):
        chunks = []
        for i in range(30):
            chunks.append({"paper_title": "BERT Paper", "content": f"b{i}"})
            chunks.append({"paper_title": "GPT Paper", "content": f"g{i}"})
        result = self.balance(chunks, {"BERT": 30, "GPT": 30}, 8, 2, 3)
        self.assertEqual(len(result), 6)
        b = sum(1 for d in result if "BERT" in d["paper_title"])
        g = sum(1 for d in result if "GPT" in d["paper_title"])
        self.assertTrue(2 <= b <= 3)
        self.assertTrue(2 <= g <= 3)

    def test_single_subject(self):
        chunks = [{"paper_title": "BERT Paper", "content": f"c{i}"} for i in range(20)]
        result = self.balance(chunks, {"BERT": 20}, 10, 3, 8)
        self.assertTrue(3 <= len(result) <= 8)


# ═══════════════════════════════════════════════════════════════════
# B6: KB 缺失匹配
# ═══════════════════════════════════════════════════════════════════

class TestKBMissing(unittest.TestCase):

    TEST_PAPERS = {
        "poisonedrag": {
            "display_name": "PoisonedRAG",
            "aliases": ["Poisoned RAG", "Knowledge Corruption Attacks"],
            "abstract": "test",
        },
        "flippedrag": {
            "display_name": "FlippedRAG",
            "aliases": ["Black-Box Opinion Manipulation"],
        },
    }

    @classmethod
    def setUpClass(cls):
        cls._path = "data/kb_missing_papers.json"
        cls._original = None
        if os.path.exists(cls._path):
            with open(cls._path) as f:
                cls._original = json.load(f)
        with open(cls._path, "w") as f:
            json.dump({"papers": cls.TEST_PAPERS}, f, ensure_ascii=False)
        from agent.react_agent import ReactAgent
        cls.agent = ReactAgent()
        cls.agent._kb_missing_cache = None

    @classmethod
    def tearDownClass(cls):
        if cls._original:
            with open(cls._path, "w") as f:
                json.dump(cls._original, f, ensure_ascii=False)
        else:
            os.remove(cls._path)

    def test_exact_match(self):
        self.assertIsNotNone(self.agent._match_kb_missing("PoisonedRAG"))

    def test_case_insensitive(self):
        self.assertIsNotNone(self.agent._match_kb_missing("poisonedrag"))

    def test_alias_match(self):
        self.assertIsNotNone(self.agent._match_kb_missing("Knowledge Corruption Attacks"))

    def test_another_paper(self):
        self.assertIsNotNone(self.agent._match_kb_missing("FlippedRAG"))

    def test_not_found(self):
        self.assertIsNone(self.agent._match_kb_missing("ELSA3D"))
        self.assertIsNone(self.agent._match_kb_missing("BERT"))


# ═══════════════════════════════════════════════════════════════════
# B7: 在线检索格式化
# ═══════════════════════════════════════════════════════════════════

class TestOnlineSearchFormat(unittest.TestCase):
    """OnlineRetrievalResult 返回格式约定"""

    def test_empty_result_message(self):
        from agent.retrieval.retrieval_pipeline import OnlineRetrievalResult
        result = OnlineRetrievalResult(text="未找到相关论文。")
        self.assertIn("未找到", result.text)

    def test_valid_paper_format(self):
        from agent.retrieval.retrieval_pipeline import OnlineRetrievalResult
        from agent.retrieval.academic_client import AcademicPaper
        paper = AcademicPaper(
            title="Test Paper About Transformers",
            authors=["Alice Smith", "Bob Jones"],
            year="2025",
            source="arXiv",
            abstract="Novel architecture.",
        )
        result = OnlineRetrievalResult(
            text="[1] Test Paper About Transformers",
            scored_results=((paper, 0.95),),
        )
        self.assertIn("[1]", result.text)
        meta = result.papers_meta()
        self.assertTrue(len(meta) > 0)


class TestThreadSafety(unittest.TestCase):

    def test_try_consume_not_exceed_max(self):
        """验证 AgentExecutionPolicy.try_consume 在多线程下不超配额"""
        from agent.execution_policy import AgentExecutionPolicy
        policy = AgentExecutionPolicy(max_tool_calls=15)
        results = []

        def consume_n(n):
            local = sum(1 for _ in range(n) if policy.try_consume())
            results.append(local)

        threads = [threading.Thread(target=consume_n, args=(5,)) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        total = sum(results)
        self.assertEqual(total, 15, f"Expected 15, got {total}")
        self.assertFalse(policy.try_consume(), "Should be exhausted")


if __name__ == "__main__":
    unittest.main(verbosity=2)
