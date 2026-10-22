
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
