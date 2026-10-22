
from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.workflow.state_machine import WorkflowState


@dataclass
class TraceEvent:
    state: str
    message: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class WorkflowTrace:
    run_id: str
    events: list[TraceEvent] = field(default_factory=list)

    def record(self, state: WorkflowState, message: str) -> None:
        """Record a state transition with its own timestamp."""
        timestamp = datetime.now(timezone.utc).isoformat()

        self.events.append(
            TraceEvent(
                state=state.value,
                message=message,
                timestamp=timestamp,
            )
        )

    def to_dict(self) -> dict:
        """Return the trace as a dictionary."""
        return {
            "run_id": self.run_id,
            "events": [
                {
                    "state": event.state,
                    "message": event.message,
                    "timestamp": event.timestamp,
                }
                for event in self.events
            ],
        }
