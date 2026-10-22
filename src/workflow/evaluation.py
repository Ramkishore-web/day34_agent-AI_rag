
import json
from pathlib import Path
from typing import Any


def load_regression_cases(
    path: str | Path = "evals/regression_cases.json",
) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as file:
        cases = json.load(file)

    if not isinstance(cases, list):
        raise ValueError("Regression dataset must be a JSON list")

    case_ids = [case.get("case_id") for case in cases]
    if any(not case_id for case_id in case_ids):
        raise ValueError("Every case must have a case_id")

    if len(case_ids) != len(set(case_ids)):
        raise ValueError("Duplicate case_id found")

    return cases


def build_evaluation_report(
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    total = len(results)
    completed = sum(r.get("actual_status") == "success" for r in results)
    expected_failures = [
        r for r in results if r.get("expected_status") == "failed"
    ]
    handled_failures = sum(
        r.get("actual_status") == "failed"
        and bool(r.get("failure_category"))
        for r in expected_failures
    )

    outputs = [
        r.get("answer", "").strip().casefold()
        for r in results
        if r.get("actual_status") == "success"
    ]
    duplicate_count = len(outputs) - len(set(outputs))

    # This is only a proxy until claims are checked against source content.
    grounded_cases = sum(
        r.get("actual_status") == "success"
        and bool(r.get("evidence_urls"))
        for r in results
    )

    return {
        "total_cases": total,
        "completion_rate": completed / total if total else 0.0,
        "groundedness_proxy_rate": (
            grounded_cases / completed if completed else 0.0
        ),
        "duplicate_rate": (
            duplicate_count / len(outputs) if outputs else 0.0
        ),
        "failure_handling_rate": (
            handled_failures / len(expected_failures)
            if expected_failures else 1.0
        ),
        "results": results,
    }
