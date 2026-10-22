
from dataclasses import asdict, dataclass, field
from time import perf_counter
from typing import Any
from uuid import uuid4


@dataclass
class RunMetrics:
    run_id: str
    correlation_id: str = field(default_factory=lambda: str(uuid4()))
    status: str = "running"
    latency_ms: float = 0.0
    tool_calls: int = 0
    tool_failures: int = 0
    failure_category: str | None = None
    token_usage: int | None = None
    estimated_cost: float | None = None

    def __post_init__(self):
        self._started_at = perf_counter()

    def record_tool_call(self, failed: bool = False) -> None:
        self.tool_calls += 1
        if failed:
            self.tool_failures += 1

    def finish(
        self,
        status: str,
        failure_category: str | None = None,
    ) -> None:
        self.status = status
        self.failure_category = failure_category
        self.latency_ms = round(
            (perf_counter() - self._started_at) * 1000, 3
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
