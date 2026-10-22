
import pytest

from src.workflow.main import run_workflow


def test_workflow_success():
    result = run_workflow(
        task="Research Python testing",
        evidence_urls=[
            "https://docs.python.org/3/library/unittest.html"
        ],
    )

    assert result["status"] == "success"
    assert result["run_id"] == "run-001"


def test_workflow_rejects_missing_evidence():
    with pytest.raises(ValueError, match="No evidence supplied"):
        run_workflow(
            task="Research Python testing",
            evidence_urls=[],
        )


def test_workflow_rejects_invalid_source_url():
    with pytest.raises(ValueError, match="failed validation"):
        run_workflow(
            task="Research Python testing",
            evidence_urls=["not-a-valid-url"],
        )

from unittest.mock import patch

import pytest

from src.workflow.main import run_workflow


def test_research_failure_is_propagated():
    with patch(
        "src.workflow.main.conduct_research",
        side_effect=RuntimeError("Research failed"),
    ):
        with pytest.raises(RuntimeError, match="Research failed"):
            run_workflow(
                task="Test research failure",
                evidence_urls=["https://example.com/evidence"],
            )
