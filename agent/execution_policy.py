"""执行策略 —— 线程安全的工具配额控制"""
import threading
from dataclasses import dataclass, field


@dataclass
class AgentExecutionPolicy:
    """Per-request 工具调用配额，线程安全。
    
    try_consume() 是唯一的配额消费入口，在 COMPARE 管线并发 subject 场景下
    保证不超过 max_tool_calls。
    """
    max_tool_calls: int = 15
    _tool_calls: int = field(default=0, init=False, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)

    def try_consume(self) -> bool:
        """尝试消耗一次配额。成功返回 True，配额耗尽返回 False。"""
        with self._lock:
            if self._tool_calls >= self.max_tool_calls:
                return False
            self._tool_calls += 1
            return True

    @property
    def remaining(self) -> int:
        with self._lock:
            return max(0, self.max_tool_calls - self._tool_calls)

    @property
    def consumed(self) -> int:
        with self._lock:
            return self._tool_calls
