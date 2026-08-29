"""S9: EvidenceBudgeter 测试"""
import unittest
from agent.evidence_budgeter import (
    TokenCounter, BudgetConfig, EvidenceBlock, EvidenceBudgeter,
    build_local_blocks, build_online_blocks, AllocationResult,
)


class TestTokenCounter(unittest.TestCase):

    def test_deepseek_maps_to_cl100k(self):
        tc = TokenCounter(model_name="deepseek-ai/DeepSeek-V3.2")
        self.assertEqual(tc.encoding, "cl100k_base")
        self.assertTrue(tc.approximate)

    def test_unknown_model_fallback(self):
        tc = TokenCounter(model_name="some-unknown-model")
        self.assertEqual(tc.encoding, "cl100k_base")

    def test_count_returns_int(self):
        tc = TokenCounter()
        result = tc.count("hello world")
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)


class TestEvidenceBlock(unittest.TestCase):

    def test_local_render(self):
        block = EvidenceBlock(
            evidence_id="local:0", source_type="local", subject_id="",
            source_order=0, quality_score=0.8,
            citation_meta={"title": "Test Paper", "section": "method",
                           "page_start": 3, "page_end": 4},
            raw_content="Some content.",
            token_cost=10,
        )
        rendered = block.render(1)
        self.assertIn("[1]", rendered)
        self.assertIn("Test Paper", rendered)
        self.assertIn("Some content.", rendered)

    def test_online_render(self):
        block = EvidenceBlock(
            evidence_id="online:0", source_type="online", subject_id="",
            source_order=0, quality_score=0.7,
            citation_meta={"title": "Online Paper", "source": "arXiv"},
            raw_content="Online content.",
            token_cost=10,
        )
        rendered = block.render(2)
        self.assertIn("[2]", rendered)
        self.assertIn("[在线]", rendered)
        self.assertIn("arXiv", rendered)


class TestBudgetAllocation(unittest.TestCase):

    def setUp(self):
        self.config = BudgetConfig(
            context_window=4096, output_reserve=512,
            safety_margin_tokens=100, target_min_local=1,
            target_min_online=1, min_quality_score=0.0,
        )
        self.counter = TokenCounter()
        self.budgeter = EvidenceBudgeter(config=self.config, counter=self.counter)

    def _make_local(self, n=3):
        blocks = []
        for i in range(n):
            blocks.append(EvidenceBlock(
                evidence_id=f"local:{i}", source_type="local", subject_id="",
                source_order=i, quality_score=0.8,
                citation_meta={"title": f"Paper {i}", "section": "method"},
                raw_content=f"Content {i}.",
                token_cost=self.counter.count(f"[N] 来源：《Paper {i}》；章节：method；页码：p.1；内容：Content {i}."),
            ))
        return blocks

    def _make_online(self, n=2):
        blocks = []
        for i in range(n):
            blocks.append(EvidenceBlock(
                evidence_id=f"online:{i}", source_type="online", subject_id="",
                source_order=i, quality_score=0.7,
                citation_meta={"title": f"Online {i}", "source": "arXiv"},
                raw_content=f"Online content {i}.",
                token_cost=self.counter.count(f"[N] [在线]《Online {i}》| 来源：arXiv\nOnline content {i}."),
            ))
        return blocks

    def test_allocation_within_budget(self):
        result = self.budgeter.allocate(
            system_prompt="You are a helpful assistant.",
            query="What is RAG?",
            local_blocks=self._make_local(2),
            online_blocks=self._make_online(1),
            online_available=True,
        )
        self.assertTrue(result.within_budget)
        self.assertGreater(len(result.selected_blocks), 0)

    def test_online_skipped_when_not_available(self):
        result = self.budgeter.allocate(
            system_prompt="Prompt",
            query="Query",
            local_blocks=self._make_local(2),
            online_blocks=self._make_online(2),
            online_available=False,
        )
        online_selected = [b for b in result.selected_blocks if b.source_type == "online"]
        self.assertEqual(len(online_selected), 0)

    def test_reference_map_has_consecutive_numbers(self):
        result = self.budgeter.allocate(
            system_prompt="Prompt",
            query="Query",
            local_blocks=self._make_local(2),
            online_available=False,
        )
        nums = [r[0] for r in result.reference_map]
        self.assertEqual(nums, list(range(1, len(nums) + 1)))

    def test_dropped_not_in_reference_map(self):
        result = self.budgeter.allocate(
            system_prompt="Prompt",
            query="Query",
            local_blocks=self._make_local(1),
            online_available=False,
        )
        selected_ids = {r[1] for r in result.reference_map}
        dropped_ids = {b.evidence_id for b in result.dropped_blocks}
        self.assertTrue(selected_ids.isdisjoint(dropped_ids))

    def test_empty_input(self):
        result = self.budgeter.allocate(
            system_prompt="Prompt",
            query="Query",
            local_blocks=[],
            online_available=False,
        )
        self.assertEqual(len(result.selected_blocks), 0)

    def test_token_usage_keys(self):
        result = self.budgeter.allocate(
            system_prompt="Prompt",
            query="Query",
            local_blocks=self._make_local(1),
            online_available=False,
        )
        for key in ("fixed", "memory", "extra", "evidence", "total"):
            self.assertIn(key, result.token_usage)

    def test_approximate_flag(self):
        result = self.budgeter.allocate(
            system_prompt="P", query="Q",
            local_blocks=[], online_available=False,
        )
        self.assertTrue(result.approximate_token_count)


if __name__ == "__main__":
    unittest.main()
