
from src.workflow.schemas import AgentHandoff, ResearchResult


def conduct_research(handoff: AgentHandoff) -> ResearchResult:
    """Create a result only when source evidence is supplied."""

    if handoff.to_agent != "researcher":
        raise ValueError("Researcher received an invalid handoff")

    if handoff.status != "success":
        raise ValueError("Cannot research a failed handoff")

    if not handoff.evidence_urls:
        raise ValueError(
            "No evidence supplied. Research cannot be completed."
        )

    return ResearchResult(
        run_id=handoff.run_id,
        answer=f"Research completed for task: {handoff.task}",
        evidence_urls=handoff.evidence_urls,
    )
