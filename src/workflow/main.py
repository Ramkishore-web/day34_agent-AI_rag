
from src.workflow.planner import create_plan
from src.workflow.researcher import conduct_research
from src.workflow.validator import validate_result


def run_workflow(
    task: str,
    evidence_urls: list[str],
    run_id: str = "run-001",
) -> dict:
    """Run planner, researcher and validator in sequence."""

    handoff = create_plan(run_id, task)

    # Supply evidence from an external research tool or test fixture.
    handoff = handoff.model_copy(
        update={"evidence_urls": evidence_urls}
    )

    result = conduct_research(handoff)

    if not validate_result(result):
        raise ValueError("Research result failed validation")

    return {
        "run_id": result.run_id,
        "status": "success",
        "answer": result.answer,
        "evidence_urls": result.evidence_urls,
    }


if __name__ == "__main__":
    output = run_workflow(
        task="Research Python testing best practices",
        evidence_urls=["https://docs.python.org/3/library/unittest.html"],
    )
    print(output)
