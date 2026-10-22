
import asyncio

from src.workflow.planner import create_plan
from src.workflow.researcher import conduct_research
from src.workflow.schemas import ResearchResult
from src.workflow.validator import validate_result
from src.workflow.state_machine import WorkflowState, transition
from src.workflow.trace import WorkflowTrace
from src.workflow.tool_executor import execute_tool


async def run_workflow_async(
    task: str,
    evidence_urls: list[str],
    run_id: str = "run-001",
    timeout_seconds: float = 5.0,
    max_attempts: int = 2,
) -> dict:
    state = WorkflowState.START
    trace = WorkflowTrace(run_id=run_id)
    trace.record(state, "Workflow started")

    try:
        # Step 1: Validate input before running tools.
        if not task.strip():
            raise ValueError("Task cannot be empty")

        if not evidence_urls:
            raise ValueError("No evidence supplied")

        # Step 2: Planning
        state = transition(state, WorkflowState.PLANNING)
        trace.record(state, "Planner created handoff")

        handoff = create_plan(run_id, task)

        # Step 3: Research
        state = transition(state, WorkflowState.RESEARCHING)
        trace.record(state, "Research started")

        handoff = handoff.model_copy(
            update={"evidence_urls": evidence_urls}
        )

        async def research_tool():
            return conduct_research(handoff)

        # Include inputs in the key so different requests
        # cannot reuse a result from another request.
        import hashlib
        import json

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
        except Exception as exc:
            from src.workflow.tool_executor import ToolOutputError

            if isinstance(exc, ToolOutputError):
                raise ValueError(
                    "Research result failed validation"
                ) from exc
            raise

            
        

        # Step 4: Validate result
        state = transition(state, WorkflowState.VALIDATING)
        trace.record(state, "Result validation started")

        if not validate_result(result):
            raise ValueError("Research result failed validation")

        # Step 5: Completed
        state = transition(state, WorkflowState.COMPLETED)
        trace.record(state, "Workflow completed")

        return {
            "run_id": result.run_id,
            "status": "success",
            "answer": result.answer,
            "evidence_urls": result.evidence_urls,
            "trace": trace.to_dict(),
        }

    except asyncio.CancelledError:
        if state not in {
            WorkflowState.COMPLETED,
            WorkflowState.FAILED,
            WorkflowState.CANCELLED,
        }:
            state = transition(state, WorkflowState.CANCELLED)

        trace.record(state, "Workflow cancelled")
        raise

    except Exception as exc:
        if state not in {
            WorkflowState.COMPLETED,
            WorkflowState.FAILED,
            WorkflowState.CANCELLED,
        }:
            state = transition(state, WorkflowState.FAILED)

        trace.record(state, f"Workflow failed: {exc}")
        raise


def run_workflow(
    task: str,
    evidence_urls: list[str],
    run_id: str = "run-001",
) -> dict:
    return asyncio.run(
        run_workflow_async(
            task=task,
            evidence_urls=evidence_urls,
            run_id=run_id,
        )
    )


if __name__ == "__main__":
    output = run_workflow(
        task="Research Python testing best practices",
        evidence_urls=[
            "https://docs.python.org/3/library/unittest.html"
        ],
    )
    print(output)
