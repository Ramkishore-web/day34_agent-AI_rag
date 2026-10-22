
from src.workflow.schemas import AgentHandoff


def create_plan(run_id: str, task: str) -> AgentHandoff:
    """Create a validated handoff from planner to researcher."""
    return AgentHandoff(
        run_id=run_id,
        task=task,
        from_agent="planner",
        to_agent="researcher",
        status="success",
        evidence_urls=[],
    )
