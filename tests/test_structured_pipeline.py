"""S8a: _execute_intent_structured 离线测试（不依赖网络）"""
import unittest
from dataclasses import replace, FrozenInstanceError

from agent.retrieval.academic_client import SearchIntent
from agent.retrieval.retrieval_pipeline import OnlineRetrievalResult


class TestSearchIntentFrozen(unittest.TestCase):

    def test_search_intent_frozen(self):
        intent = SearchIntent(candidate="Test", candidate_type="acronym")
        with self.assertRaises(FrozenInstanceError):
            intent.keyword = "new"

    def test_replace_creates_new_intent(self):
        i1 = SearchIntent(candidate="Test")
        i2 = replace(i1, keyword="new_keyword")
        self.assertEqual(i1.keyword, "")
        self.assertEqual(i2.keyword, "new_keyword")
        self.assertIsNot(i1, i2)


class TestOnlineRetrievalResult(unittest.TestCase):

    def test_stop_stage_none_by_default(self):
        result = OnlineRetrievalResult(
            text="test",
            scored_results=(),
            stage_results=(),
            early_stopped=False,
            stop_stage=None,
            executed_stages=(),
            papers_per_stage=(),
            intent_candidate="",
            intent_candidate_type="unknown",
        )
        self.assertIsNone(result.stop_stage)

    def test_scored_results_is_tuple(self):
        result = OnlineRetrievalResult(
            text="test", scored_results=((object(), 0.9),),
            stage_results=(), early_stopped=False, stop_stage=None,
            executed_stages=(), papers_per_stage=(),
            intent_candidate="", intent_candidate_type="unknown",
        )
        self.assertIsInstance(result.scored_results, tuple)

    def test_stage_results_is_tuple(self):
        result = OnlineRetrievalResult(
            text="test", scored_results=(),
            stage_results=(), early_stopped=False, stop_stage=None,
            executed_stages=(), papers_per_stage=(),
            intent_candidate="", intent_candidate_type="unknown",
        )
        self.assertIsInstance(result.stage_results, tuple)

    def test_papers_meta_empty(self):
        result = OnlineRetrievalResult(
            text="test", scored_results=(),
            stage_results=(), early_stopped=False, stop_stage=None,
            executed_stages=(), papers_per_stage=(),
            intent_candidate="", intent_candidate_type="unknown",
        )
        self.assertEqual(result.papers_meta(), [])

    def test_text_from_str(self):
        result = OnlineRetrievalResult(
            text="hello world", scored_results=(),
            stage_results=(), early_stopped=False, stop_stage=None,
            executed_stages=(), papers_per_stage=(),
            intent_candidate="", intent_candidate_type="unknown",
        )
        self.assertEqual(str(result), "hello world")

    def test_field_types(self):
        result = OnlineRetrievalResult(
            text="", scored_results=(), stage_results=(),
            early_stopped=False, stop_stage=1,
            executed_stages=(1, 2), papers_per_stage=(3, 0),
            intent_candidate="BERT", intent_candidate_type="acronym",
        )
        self.assertIsInstance(result.executed_stages, tuple)
        self.assertIsInstance(result.papers_per_stage, tuple)
        self.assertEqual(result.stop_stage, 1)
        self.assertEqual(result.intent_candidate, "BERT")


class TestPipelineImport(unittest.TestCase):
    """验证模块可正确导入，_execute_intent_structured 方法存在"""

    def test_method_exists(self):
        from agent.retrieval.retrieval_pipeline import OnlineRetrievalPipeline
        self.assertTrue(hasattr(OnlineRetrievalPipeline, "_execute_intent_structured"))
        self.assertTrue(hasattr(OnlineRetrievalPipeline, "_score_and_check"))
        self.assertTrue(hasattr(OnlineRetrievalPipeline, "_format_scored"))


if __name__ == "__main__":
    unittest.main()
