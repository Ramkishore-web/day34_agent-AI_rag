
import pytest
from pydantic import ValidationError

from src.workflow.schemas import AgentHandoff, ResearchResult


def test_valid_handoff():
    handoff = AgentHandoff(
        run_id="run-001",
        task="Research Python testing",
        from_agent="planner",
        to_agent="researcher",
        status="success",
    )
    assert handoff.run_id == "run-001"


def test_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        AgentHandoff(
            run_id="run-001",
            task="Research",
            from_agent="planner",
            to_agent="researcher",
            status="success",
            unexpected="not allowed",
        )


def test_rejects_empty_task():
    with pytest.raises(ValidationError):
        AgentHandoff(
            run_id="run-001",
            task="",
            from_agent="planner",
            to_agent="researcher",
            status="success",
        )


def test_research_requires_evidence():
    with pytest.raises(ValidationError):
        ResearchResult(
            run_id="run-001",
            answer="Python is useful",
            evidence_urls=[],
        )
