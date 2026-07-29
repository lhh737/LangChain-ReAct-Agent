"""在线学术检索重试策略：指数退避 + Retry-After + 抖动 + 按源配置"""
import random
import time
from dataclasses import dataclass, field
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
from typing import Callable

from utils.config_handler import agent_conf
from utils.logger_handler import logger


@dataclass
class SourceRetryConfig:
    max_retries: int = 2
    base_delay: float = 1.0
    max_delay: float = 30.0
    jitter: float = 0.25

    @classmethod
    def from_dict(cls, d: dict) -> "SourceRetryConfig":
        return cls(
            max_retries=int(d.get("max_retries", 2)),
            base_delay=float(d.get("base_delay", 1.0)),
            max_delay=float(d.get("max_delay", 30.0)),
            jitter=float(d.get("jitter", 0.25)),
        )


@dataclass
class RetryPolicy:
    default: SourceRetryConfig
    sources: dict[str, SourceRetryConfig]
    retry_on_status: set[int]
    retry_on_exceptions: set[str]
    valid_empty_requires_retry: bool

    # 可注入依赖
    sleep_fn: Callable[[float], None] = field(default=time.sleep, repr=False)
    random_fn: Callable[[], float] = field(default=random.random, repr=False)
    clock_fn: Callable[[], float] = field(default=time.monotonic, repr=False)

    @classmethod
    def from_config(cls, config: dict | None = None) -> "RetryPolicy":
        if config is None:
            config = agent_conf.get("retrieval_retry", {})
        default_cfg = SourceRetryConfig.from_dict(config.get("default", {}))
        sources = {}
        for name, src_cfg in config.get("sources", {}).items():
            merged = config.get("default", {}).copy()
            merged.update(src_cfg)
            sources[name] = SourceRetryConfig.from_dict(merged)
        return cls(
            default=default_cfg,
            sources=sources,
            retry_on_status=set(config.get("retry_on_status", [429, 502, 503, 504])),
            retry_on_exceptions=set(config.get("retry_on_exceptions",
                ["TimeoutException", "ConnectError", "ReadError", "RemoteProtocolError"])),
            valid_empty_requires_retry=config.get("valid_empty_requires_retry", True),
        )

    def for_source(self, source: str) -> SourceRetryConfig:
        return self.sources.get(source, self.default)

    def should_retry(self, status: str, http_status: int | None,
                     exception: Exception | None, attempt: int) -> bool:
        cfg = self.default  # 状态判断不按源区分
        if attempt > cfg.max_retries:
            return False
        if exception is not None:
            exc_name = type(exception).__name__
            return exc_name in self.retry_on_exceptions
        if http_status == 429 or (http_status is not None and http_status >= 500):
            return http_status in self.retry_on_status
        return False

    def parse_retry_after(self, headers: dict) -> float | None:
        value = headers.get("Retry-After", "")
        if not value:
            return None
        try:
            return float(value)
        except ValueError:
            pass
        try:
            target = parsedate_to_datetime(value)
            now = datetime.now(timezone.utc)
            return max(0.0, (target - now).total_seconds())
        except Exception:
            pass
        return None

    def backoff_delay(self, attempt: int, source: str = "",
                      retry_after: float | None = None) -> float:
        if retry_after is not None and retry_after > 0:
            cfg = self.for_source(source)
            return max(0.1, min(retry_after, cfg.max_delay))
        cfg = self.for_source(source)
        delay = cfg.base_delay * (2 ** (attempt - 1))
        jitter_amount = delay * cfg.jitter * (self.random_fn() * 2 - 1)
        return max(0.1, min(delay + jitter_amount, cfg.max_delay))


# 模块级单例，惰性加载
_policy: RetryPolicy | None = None


def get_retry_policy() -> RetryPolicy:
    global _policy
    if _policy is None:
        _policy = RetryPolicy.from_config()
        logger.info(f"[RetryPolicy] loaded: default max_retries={_policy.default.max_retries}")
    return _policy
