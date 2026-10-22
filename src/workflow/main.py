
import asyncio
import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from src.workflow.planner import create_plan
from src.workflow.researcher import conduct_research
from src.workflow.schemas import ResearchResult
from src.workflow.validator import validate_result
from src.workflow.state_machine import WorkflowState, transition
from src.workflow.trace import WorkflowTrace
from src.workflow.tool_executor import (
    execute_tool,
    ToolExecutionError,
    ToolTimeoutError,
    ToolOutputError,
)
from src.workflow.persistence import persist_run, DEFAULT_STORAGE_DIR
from src.workflow.metrics import RunMetrics


def _save_snapshot(
    run_id: str,
    payload: dict[str, Any],
    storage_dir: str | Path,
) -> None:
    """Persist a workflow snapshot."""
    persist_run(run_id, payload, storage_dir=storage_dir)


def _failure_category(exc: Exception) -> str:
    """Classify failures for monitoring and evaluation."""
    if isinstance(exc, ToolTimeoutError):
        return "tool_timeout"

    if isinstance(exc, ToolOutputError):
        return "output_validation"

    if isinstance(exc, ToolExecutionError):
        return "tool_execution"

    if isinstance(exc, ValueError):
        return "input_or_result_validation"

    return "unexpected_error"


async def run_workflow_async(
    task: str,
    evidence_urls: list[str],
    run_id: str = "run-001",
    timeout_seconds: float = 5.0,
    max_attempts: int = 2,
    storage_dir: str | Path = DEFAULT_STORAGE_DIR,
) -> dict:
    state = WorkflowState.START
    trace = WorkflowTrace(run_id=run_id)
    metrics = RunMetrics(run_id=run_id)

    trace.record(
        state,
        f"Workflow started; correlation_id={metrics.correlation_id}",
    )

    try:
        # Step 1: Validate input.
        if not isinstance(task, str) or not task.strip():
            raise ValueError("Task cannot be empty")

        if not isinstance(evidence_urls, list) or not evidence_urls:
            raise ValueError("No evidence supplied")

        for url in evidence_urls:
            if not isinstance(url, str):
                raise ValueError(
                    "Research result failed validation: invalid evidence URL"
                )

            parsed = urlparse(url)

            if (
                parsed.scheme != "https"
                or not parsed.netloc
                or not parsed.hostname
            ):
                raise ValueError(
                    "Research result failed validation: invalid evidence URL"
                )

        # Step 2: Planning.
        state = transition(state, WorkflowState.PLANNING)
        trace.record(state, "Planner created handoff")

        handoff = create_plan(run_id, task)

        # Step 3: Research.
        state = transition(state, WorkflowState.RESEARCHING)
        trace.record(state, "Research started")

        handoff = handoff.model_copy(
            update={"evidence_urls": evidence_urls}
        )

        async def research_tool():
            return conduct_research(handoff)

        cache_input = json.dumps(
            {
                "task": task,
                "evidence_urls": evidence_urls,
            },
            sort_keys=True,
        )

        input_hash = hashlib.sha256(
            cache_input.encode("utf-8")
        ).hexdigest()

        try:
            result = await execute_tool(
                research_tool,
                idempotency_key=f"{run_id}:research:{input_hash}",
                validate_output=lambda value: (
                    isinstance(value, ResearchResult)
                    and validate_result(value)
                ),
                timeout_seconds=timeout_seconds,
                max_attempts=max_attempts,
            )
        except Exception:
            metrics.record_tool_call(failed=True)
            raise
        else:
            metrics.record_tool_call()

        # Step 4: Validate result.
        state = transition(state, WorkflowState.VALIDATING)
        trace.record(state, "Result validation started")

        if not validate_result(result):
            raise ValueError("Research result failed validation")

        # Step 5: Complete workflow.
        state = transition(state, WorkflowState.COMPLETED)
        trace.record(state, "Workflow completed")

        metrics.finish("success")

        output = {
            "run_id": result.run_id,
            "status": "success",
            "answer": result.answer,
            "evidence_urls": result.evidence_urls,
            "trace": trace.to_dict(),
            "metrics": metrics.to_dict(),
        }

        _save_snapshot(
            run_id,
            {
                "task": task,
                **output,
            },
            storage_dir,
        )

        return output

    except asyncio.CancelledError:
        if state not in {
            WorkflowState.COMPLETED,
            WorkflowState.FAILED,
            WorkflowState.CANCELLED,
        }:
            state = transition(state, WorkflowState.CANCELLED)

        trace.record(state, "Workflow cancelled")
        metrics.finish("cancelled", failure_category="cancelled")

        try:
            _save_snapshot(
                run_id,
                {
                    "task": task,
                    "status": "cancelled",
                    "evidence_urls": evidence_urls,
                    "trace": trace.to_dict(),
                    "metrics": metrics.to_dict(),
                },
                storage_dir,
            )
        except Exception:
            pass

        raise

    except Exception as exc:
        if state not in {
            WorkflowState.COMPLETED,
            WorkflowState.FAILED,
            WorkflowState.CANCELLED,
        }:
            state = transition(state, WorkflowState.FAILED)

        category = _failure_category(exc)

        trace.record(
            state,
            f"Workflow failed: {exc}; failure_category={category}",
        )

        metrics.finish(
            status="failed",
            failure_category=category,
        )

        try:
            _save_snapshot(
                run_id,
                {
                    "task": task,
                    "status": "failed",
                    "error": str(exc),
                    "failure_category": category,
                    "evidence_urls": evidence_urls,
                    "trace": trace.to_dict(),
                    "metrics": metrics.to_dict(),
                },
                storage_dir,
            )
        except Exception:
            pass

        raise


def run_workflow(
    task: str,
    evidence_urls: list[str],
    run_id: str = "run-001",
    storage_dir: str | Path = DEFAULT_STORAGE_DIR,
) -> dict:
    return asyncio.run(
        run_workflow_async(
            task=task,
            evidence_urls=evidence_urls,
            run_id=run_id,
            storage_dir=storage_dir,
        )
    )


if __name__ == "__main__":
    output = run_workflow(
        task="Research Python testing best practices",
        evidence_urls=[
            "https://docs.python.org/3/library/unittest.html"
        ],
        run_id="day4-demo",
    )
    print(json.dumps(output, indent=2, ensure_ascii=False))
