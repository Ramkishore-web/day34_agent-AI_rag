
from enum import Enum


class WorkflowState(str, Enum):
    START = "start"
    PLANNING = "planning"
    RESEARCHING = "researching"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


ALLOWED_TRANSITIONS = {
    WorkflowState.START: {
        WorkflowState.PLANNING,
        WorkflowState.FAILED,
        WorkflowState.CANCELLED,
    },
    WorkflowState.PLANNING: {
        WorkflowState.RESEARCHING,
        WorkflowState.FAILED,
        WorkflowState.CANCELLED,
    },
    WorkflowState.RESEARCHING: {
        WorkflowState.VALIDATING,
        WorkflowState.FAILED,
        WorkflowState.CANCELLED,
    },
    WorkflowState.VALIDATING: {
        WorkflowState.COMPLETED,
        WorkflowState.FAILED,
        WorkflowState.CANCELLED,
    },
    WorkflowState.COMPLETED: set(),
    WorkflowState.FAILED: set(),
    WorkflowState.CANCELLED: set(),
}


def transition(
    current: WorkflowState,
    target: WorkflowState,
) -> WorkflowState:
    if target not in ALLOWED_TRANSITIONS[current]:
        raise ValueError(
            f"Invalid transition: {current.value} -> {target.value}"
        )
    return target
