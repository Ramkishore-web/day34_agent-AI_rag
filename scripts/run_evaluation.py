
import asyncio
import json
from pathlib import Path

from src.workflow.main import run_workflow_async
from src.workflow.evaluation import (
    load_regression_cases,
    build_evaluation_report,
)


async def main():
    # Load regression test cases
    cases = load_regression_cases()
    results = []

    for case in cases:
        case_id = case["case_id"]
        print(f"Running evaluation: {case_id}")

        try:
            output = await run_workflow_async(
                task=case["task"],
                evidence_urls=case["evidence_urls"],
                run_id=f"eval-{case_id}",
            )

            actual_status = output["status"]
            answer = output.get("answer", "")
            evidence_urls = output.get("evidence_urls", [])
            failure_category = None

        except Exception as exc:
            actual_status = "failed"
            answer = ""
            evidence_urls = []

            message = str(exc).lower()

            if any(word in message for word in ("evidence", "task", "url")):
                failure_category = "input_or_result_validation"
            else:
                failure_category = "unexpected_error"

            print(f"  Failure: {exc}")

        results.append({
            "case_id": case_id,
            "expected_status": case["expected_status"],
            "actual_status": actual_status,
            "failure_category": failure_category,
            "answer": answer,
            "evidence_urls": evidence_urls,
            "status_matches": actual_status == case["expected_status"],
        })

    report = build_evaluation_report(results)

    # Add the expected-vs-actual comparison to the report
    report["passed_cases"] = sum(
        result["status_matches"] for result in results
    )
    report["failed_cases"] = sum(
        not result["status_matches"] for result in results
    )

    report_path = Path("evals/evaluation_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n===== Evaluation Report =====")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\nReport saved to: {report_path.resolve()}")


if __name__ == "__main__":
    asyncio.run(main())
