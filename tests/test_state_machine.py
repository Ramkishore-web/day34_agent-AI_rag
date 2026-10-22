
import pytest

from src.workflow.state_machine import WorkflowState, transition


def test_valid_transition():
    assert transition(
        WorkflowState.START,
        WorkflowState.PLANNING
    ) == WorkflowState.PLANNING


def test_successful_workflow_path():
    state = WorkflowState.START

    for next_state in [
        WorkflowState.PLANNING,
        WorkflowState.RESEARCHING,
        WorkflowState.VALIDATING,
        WorkflowState.COMPLETED,
    ]:
        state = transition(state, next_state)

    assert state == WorkflowState.COMPLETED


def test_invalid_transition_rejected():
    with pytest.raises(ValueError, match="Invalid transition"):
        transition(WorkflowState.START, WorkflowState.COMPLETED)


def test_terminal_state_cannot_continue():
    with pytest.raises(ValueError, match="Invalid transition"):
        transition(WorkflowState.COMPLETED, WorkflowState.PLANNING)

def test_workflow_can_be_cancelled():
    state = transition(
        WorkflowState.RESEARCHING,
        WorkflowState.CANCELLED,
    )

    assert state == WorkflowState.CANCELLED


def test_cancelled_state_cannot_continue():
    with pytest.raises(ValueError):
        transition(
            WorkflowState.CANCELLED,
            WorkflowState.COMPLETED,
        )
