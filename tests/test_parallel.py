"""S8c: 五源并行化测试"""
import unittest
from unittest.mock import patch, MagicMock
from agent.retrieval.academic_client import (
    AcademicDataClient, SearchIntent, SourceSearchResult, AcademicPaper,
)


class TestSearchStageParallel(unittest.TestCase):

    def setUp(self):
        self.client = AcademicDataClient()

    def _make_mock_fetch(self, delays=None):
        """创建 mock _fetch_source_result"""
        import time as _time
        calls = []

        def fake_fetch(name, fn, intent, stage, max_per_source, fallback_variant):
            calls.append(name)
            if delays and name in delays:
                _time.sleep(delays[name])
            return SourceSearchResult(
                source=name, stage=stage,
                actual_query="test", status="ok",
                papers=[AcademicPaper(title=f"Paper from {name}", source=name)],
            )

        return fake_fetch, calls

    def test_serial_disabled(self):
        """enabled=False 时走串行"""
        fake, recorded = self._make_mock_fetch()
        with patch.object(self.client, '_fetch_source_result', fake):
            results = self.client.search_stage(
                SearchIntent(candidate="test"), stage=1)
        self.assertEqual(len(results), 5)
        # 串行时按 sources 顺序
        self.assertEqual([r.source for r in results],
                         ["arxiv", "crossref", "dblp", "openalex", "semantic_scholar"])

    def test_parallel_enabled_preserves_order(self):
        """并行时按原始 sources 索引顺序恢复"""
        from utils.config_handler import agent_conf
        original = agent_conf.get("retrieval_parallel", {}).copy()

        try:
            agent_conf["retrieval_parallel"] = {"enabled": True, "max_workers": 3}
            fake, recorded = self._make_mock_fetch()
            with patch.object(self.client, '_fetch_source_result', fake):
                results = self.client.search_stage(
                    SearchIntent(candidate="test"), stage=1)
            # 结果顺序应与 sources 列表一致
            self.assertEqual([r.source for r in results],
                             ["arxiv", "crossref", "dblp", "openalex", "semantic_scholar"])
        finally:
            agent_conf["retrieval_parallel"] = original

    def test_source_exception_preserved(self):
        """单源异常，其余正常返回，且失败来源有错误记录"""
        import time as _t
        def fake_with_error(name, fn, intent, stage, max_per_source, fallback_variant):
            if name == "crossref":
                # 模拟 _fetch_source_result 内部捕获异常并返回错误结果
                return SourceSearchResult(
                    source=name, stage=stage,
                    actual_query="", status="http_error",
                    error="test error", elapsed=0.0,
                )
            return SourceSearchResult(
                source=name, stage=stage,
                actual_query="test", status="ok",
                papers=[AcademicPaper(title=f"Paper from {name}", source=name)],
            )

        from utils.config_handler import agent_conf
        original = agent_conf.get("retrieval_parallel", {}).copy()
        try:
            agent_conf["retrieval_parallel"] = {"enabled": True, "max_workers": 3}
            with patch.object(self.client, '_fetch_source_result', fake_with_error):
                results = self.client.search_stage(
                    SearchIntent(candidate="test"), stage=1)
            # 4 个正常 + 1 个异常 = 5 个结果
            self.assertEqual(len(results), 5)
            # 异常来源有错误状态
            crossref_result = [r for r in results if r.source == "crossref"][0]
            self.assertEqual(crossref_result.status, "http_error")
            self.assertIsNotNone(crossref_result.error)
        finally:
            agent_conf["retrieval_parallel"] = original

    def test_source_returns_none_skipped(self):
        """某源不支持该 stage 返回 None 时不阻塞其他源"""
        def fake_with_none(name, fn, intent, stage, max_per_source, fallback_variant):
            if name == "dblp":
                return None
            return SourceSearchResult(
                source=name, stage=stage,
                actual_query="test", status="ok",
                papers=[AcademicPaper(title=f"Paper from {name}", source=name)],
            )

        from utils.config_handler import agent_conf
        original = agent_conf.get("retrieval_parallel", {}).copy()
        try:
            agent_conf["retrieval_parallel"] = {"enabled": True, "max_workers": 3}
            with patch.object(self.client, '_fetch_source_result', fake_with_none):
                results = self.client.search_stage(
                    SearchIntent(candidate="test"), stage=1)
            self.assertEqual(len(results), 4)  # dblp 被跳过
            sources = [r.source for r in results]
            self.assertNotIn("dblp", sources)
        finally:
            agent_conf["retrieval_parallel"] = original

    def test_disabled_serial_fallback(self):
        """配置关闭时完全走串行路径"""
        from utils.config_handler import agent_conf
        original = agent_conf.get("retrieval_parallel", {}).copy()
        try:
            agent_conf["retrieval_parallel"] = {"enabled": False}
            fake, recorded = self._make_mock_fetch()
            with patch.object(self.client, '_fetch_source_result', fake):
                self.client.search_stage(SearchIntent(candidate="test"), stage=1)
            self.assertEqual(len(recorded), 5)
        finally:
            agent_conf["retrieval_parallel"] = original


if __name__ == "__main__":
    unittest.main()
