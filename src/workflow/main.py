
from src.workflow.planner import create_plan
from src.workflow.researcher import conduct_research
from src.workflow.validator import validate_result
from src.workflow.state_machine import WorkflowState, transition
from src.workflow.trace import WorkflowTrace


def run_workflow(
    task: str,
    evidence_urls: list[str],
    run_id: str = "run-001",
) -> dict:
    """Run the workflow and record execution events."""

    state = WorkflowState.START
    trace = WorkflowTrace(run_id=run_id)
    trace.record(state, "Workflow started")

    try:
        state = transition(state, WorkflowState.PLANNING)
        trace.record(state, "Planner created handoff")

        handoff = create_plan(run_id, task)

        state = transition(state, WorkflowState.RESEARCHING)
        trace.record(state, "Research started")

        handoff = handoff.model_copy(
            update={"evidence_urls": evidence_urls}
        )
        result = conduct_research(handoff)

        state = transition(state, WorkflowState.VALIDATING)
        trace.record(state, "Result validation started")

        if not validate_result(result):
            raise ValueError("Research result failed validation")

        state = transition(state, WorkflowState.COMPLETED)
        trace.record(state, "Workflow completed")

        return {
            "run_id": result.run_id,
            "status": "success",
            "answer": result.answer,
            "evidence_urls": result.evidence_urls,
            "trace": trace.to_dict(),
        }

    except Exception as exc:
        if state not in {
            WorkflowState.COMPLETED,
            WorkflowState.FAILED,
        }:
            state = transition(state, WorkflowState.FAILED)

        trace.record(state, f"Workflow failed: {exc}")
        raise


if __name__ == "__main__":
    output = run_workflow(
        task="Research Python testing best practices",
        evidence_urls=[
            "https://docs.python.org/3/library/unittest.html"
        ],
    )
    print(output)
