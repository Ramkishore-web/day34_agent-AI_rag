
import json
import pytest

from src.workflow.evaluation import (
    load_regression_cases,
    build_evaluation_report,
)


def test_regression_dataset_loads():
    cases = load_regression_cases()
    assert len(cases) >= 1


def test_duplicate_case_ids_are_rejected(tmp_path):
    path = tmp_path / "cases.json"
    path.write_text(
        json.dumps([
            {"case_id": "same"},
            {"case_id": "same"},
        ]),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate"):
        load_regression_cases(path)


def test_evaluation_report_metrics():
    results = [
        {
            "actual_status": "success",
            "expected_status": "success",
            "answer": "same answer",
            "evidence_urls": ["https://docs.python.org/3/"],
        },
        {
            "actual_status": "success",
            "expected_status": "success",
            "answer": "same answer",
            "evidence_urls": ["https://docs.python.org/3/"],
        },
        {
            "actual_status": "failed",
            "expected_status": "failed",
            "failure_category": "input_validation",
        },
    ]

    report = build_evaluation_report(results)

    assert report["total_cases"] == 3
    assert report["completion_rate"] == pytest.approx(2 / 3)
    assert report["duplicate_rate"] == pytest.approx(0.5)
    assert report["failure_handling_rate"] == 1.0
