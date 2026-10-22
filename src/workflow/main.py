
from src.workflow.planner import create_plan
from src.workflow.researcher import conduct_research
from src.workflow.validator import validate_result
from src.workflow.state_machine import WorkflowState, transition


def run_workflow(
    task: str,
    evidence_urls: list[str],
    run_id: str = "run-001",
) -> dict:
    """Run the workflow with validated state transitions."""

    state = WorkflowState.START

    try:
        # Step 1: Start planning
        state = transition(state, WorkflowState.PLANNING)
        handoff = create_plan(run_id, task)

        # Step 2: Start research
        state = transition(state, WorkflowState.RESEARCHING)

        # Supply evidence from an external tool or test fixture.
        handoff = handoff.model_copy(
            update={"evidence_urls": evidence_urls}
        )

        result = conduct_research(handoff)

        # Step 3: Validate the research result
        state = transition(state, WorkflowState.VALIDATING)

        if not validate_result(result):
            raise ValueError("Research result failed validation")

        # Step 4: Mark workflow as completed
        state = transition(state, WorkflowState.COMPLETED)

        return {
            "run_id": result.run_id,
            "status": "success",
            "answer": result.answer,
            "evidence_urls": result.evidence_urls,
        }

    except Exception:
        # Any workflow error moves the current state to FAILED.
        if state not in {
            WorkflowState.COMPLETED,
            WorkflowState.FAILED,
        }:
            state = transition(state, WorkflowState.FAILED)

        raise


if __name__ == "__main__":
    output = run_workflow(
        task="Research Python testing best practices",
        evidence_urls=[
            "https://docs.python.org/3/library/unittest.html"
        ],
    )
    print(output)
