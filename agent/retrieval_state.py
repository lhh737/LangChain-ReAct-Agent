"""检索状态机 — 管理本地 KB miss 检测、在线结果门控、质量信号评估"""
from dataclasses import dataclass, field


@dataclass
class AgentRetrievalState:
    """每个 query 执行周期的检索状态（execute_stream 入口处重置）"""
    miss_count: int = 0
    queries_issued: list[str] = field(default_factory=list)
    local_kb_disabled: bool = False
    online_results_obtained: bool = False
    quality_signals: list[bool] = field(default_factory=list)

    def reset(self):
        self.miss_count = 0
        self.queries_issued.clear()
        self.local_kb_disabled = False
        self.online_results_obtained = False
        self.quality_signals.clear()

    def record_local_kb_hit(self):
        self.miss_count = 0
        self.quality_signals.clear()

    def record_local_kb_miss(self) -> bool:
        self.miss_count += 1
        if self.miss_count >= 2:
            self.local_kb_disabled = True
            return True
        return False

    def record_online_search(self):
        self.online_results_obtained = True

    def should_skip_local_kb(self, paper_title: str, kb_missing_index: set) -> bool:
        return paper_title.lower() in {t.lower() for t in kb_missing_index}

    def record_quality_signals(self, signals: list[bool]):
        self.quality_signals = signals

    def is_soft_miss(self) -> bool:
        if not self.quality_signals:
            return False
        return sum(1 for s in self.quality_signals if not s) >= 2
