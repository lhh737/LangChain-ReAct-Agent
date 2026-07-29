"""重试策略测试：配置加载、Retry-After、退避、抖动、按源配置、状态区分"""
import time as _time
import unittest
from agent.retrieval.retry_policy import (
    RetryPolicy, SourceRetryConfig, get_retry_policy,
)


class TestSourceRetryConfig(unittest.TestCase):

    def test_from_dict_defaults(self):
        cfg = SourceRetryConfig.from_dict({})
        self.assertEqual(cfg.max_retries, 2)
        self.assertEqual(cfg.base_delay, 1.0)

    def test_from_dict_override(self):
        cfg = SourceRetryConfig.from_dict({"max_retries": 5, "base_delay": 3.0})
        self.assertEqual(cfg.max_retries, 5)
        self.assertEqual(cfg.base_delay, 3.0)


class TestRetryPolicyLoad(unittest.TestCase):

    def test_load_from_config(self):
        policy = get_retry_policy()
        self.assertEqual(policy.default.max_retries, 2)
        self.assertIn("arxiv", policy.sources)
        self.assertEqual(policy.sources["arxiv"].base_delay, 3.0)

    def test_for_source_fallback(self):
        policy = get_retry_policy()
        cfg = policy.for_source("nonexistent")
        self.assertEqual(cfg.max_retries, policy.default.max_retries)


class TestRetryAfter(unittest.TestCase):

    def setUp(self):
        self.policy = get_retry_policy()

    def test_seconds(self):
        result = self.policy.parse_retry_after({"Retry-After": "120"})
        self.assertEqual(result, 120.0)

    def test_empty(self):
        self.assertIsNone(self.policy.parse_retry_after({}))
        self.assertIsNone(self.policy.parse_retry_after({"Retry-After": ""}))

    def test_http_date_past(self):
        # 过去的日期 → 0
        result = self.policy.parse_retry_after(
            {"Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"}
        )
        self.assertEqual(result, 0.0)


class TestBackoff(unittest.TestCase):

    def setUp(self):
        self.policy = RetryPolicy(
            default=SourceRetryConfig(max_retries=2, base_delay=1.0, jitter=0.0),
            sources={},
            retry_on_status={429, 502, 503, 504},
            retry_on_exceptions={"TimeoutException"},
            valid_empty_requires_retry=True,
        )

    def test_no_jitter(self):
        delay = self.policy.backoff_delay(1, retry_after=None)
        self.assertAlmostEqual(delay, 1.0, delta=0.01)
        delay = self.policy.backoff_delay(2, retry_after=None)
        self.assertAlmostEqual(delay, 2.0, delta=0.01)

    def test_with_jitter_range(self):
        policy_j = RetryPolicy(
            default=SourceRetryConfig(max_retries=3, base_delay=1.0, jitter=0.25),
            sources={},
            retry_on_status=set(),
            retry_on_exceptions=set(),
            valid_empty_requires_retry=False,
            random_fn=lambda: 0.5,  # fixed random
        )
        delay = policy_j.backoff_delay(1)
        self.assertAlmostEqual(delay, 1.0, delta=0.26)

    def test_respects_max_delay(self):
        policy_max = RetryPolicy(
            default=SourceRetryConfig(max_retries=5, base_delay=10.0, max_delay=5.0, jitter=0.0),
            sources={},
            retry_on_status=set(),
            retry_on_exceptions=set(),
            valid_empty_requires_retry=False,
        )
        delay = policy_max.backoff_delay(3)
        self.assertLessEqual(delay, 5.0)

    def test_retry_after_priority(self):
        delay = self.policy.backoff_delay(1, retry_after=3.0)
        self.assertAlmostEqual(delay, 3.0, delta=0.01)

    def test_sleep_fn_called(self):
        called = [0]
        policy_sleep = RetryPolicy(
            default=SourceRetryConfig(max_retries=1, base_delay=0.01, jitter=0.0),
            sources={},
            retry_on_status=set(),
            retry_on_exceptions=set(),
            valid_empty_requires_retry=False,
            sleep_fn=lambda s: called.__setitem__(0, called[0] + 1),
        )
        policy_sleep.sleep_fn(policy_sleep.backoff_delay(1))
        self.assertEqual(called[0], 1)


class TestShouldRetry(unittest.TestCase):

    def setUp(self):
        self.policy = get_retry_policy()

    def test_429_retried(self):
        self.assertTrue(self.policy.should_retry("rate_limited", 429, None, 1))

    def test_503_retried(self):
        self.assertTrue(self.policy.should_retry("http_error", 503, None, 1))

    def test_403_not_retried(self):
        self.assertFalse(self.policy.should_retry("http_error", 403, None, 1))

    def test_timeout_retried(self):
        exc = __import__("httpx", fromlist=["TimeoutException"]).TimeoutException("timeout")
        self.assertTrue(self.policy.should_retry("timeout", None, exc, 1))

    def test_exceed_max_retries(self):
        cfg = self.policy.for_source("crossref")  # max_retries=1
        # attempt 2 > max_retries 1 → should not retry
        self.assertFalse(self.policy.should_retry("timeout", None,
                          Exception("x"), cfg.max_retries + 1))


if __name__ == "__main__":
    unittest.main()
