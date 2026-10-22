
from enum import Enum


class WorkflowState(str, Enum):
    START = "start"
    PLANNING = "planning"
    RESEARCHING = "researching"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"


ALLOWED_TRANSITIONS = {
    WorkflowState.START: {
        WorkflowState.PLANNING,
        WorkflowState.FAILED,
    },
    WorkflowState.PLANNING: {
        WorkflowState.RESEARCHING,
        WorkflowState.FAILED,
    },
    WorkflowState.RESEARCHING: {
        WorkflowState.VALIDATING,
        WorkflowState.FAILED,
    },
    WorkflowState.VALIDATING: {
        WorkflowState.COMPLETED,
        WorkflowState.FAILED,
    },
    WorkflowState.COMPLETED: set(),
    WorkflowState.FAILED: set(),
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
