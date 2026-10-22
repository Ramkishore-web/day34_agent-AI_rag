
import asyncio

import pytest

from src.workflow.tool_executor import (
    ToolOutputError,
    ToolTimeoutError,
    execute_tool,
)


@pytest.mark.asyncio
async def test_successful_tool_output():
    async def tool():
        return {"answer": "ok"}

    result = await execute_tool(
        tool,
        idempotency_key="success-001",
        validate_output=lambda value: (
            isinstance(value, dict) and "answer" in value
        ),
    )

    assert result == {"answer": "ok"}


@pytest.mark.asyncio
async def test_timeout_fails_after_retry_budget():
    calls = 0

    async def slow_tool():
        nonlocal calls
        calls += 1
        await asyncio.sleep(0.1)
        return "late"

    with pytest.raises(ToolTimeoutError):
        await execute_tool(
            slow_tool,
            idempotency_key="timeout-001",
            validate_output=lambda value: isinstance(value, str),
            timeout_seconds=0.01,
            max_attempts=2,
        )

    assert calls == 2


@pytest.mark.asyncio
async def test_malformed_output_is_rejected():
    async def tool():
        return {"unexpected": "data"}

    with pytest.raises(ToolOutputError):
        await execute_tool(
            tool,
            idempotency_key="malformed-001",
            validate_output=lambda value: "answer" in value,
        )


@pytest.mark.asyncio
async def test_same_key_reuses_successful_result():
    calls = 0

    async def tool():
        nonlocal calls
        calls += 1
        return "cached"

    first = await execute_tool(
        tool,
        idempotency_key="cache-001",
        validate_output=lambda value: isinstance(value, str),
    )
    second = await execute_tool(
        tool,
        idempotency_key="cache-001",
        validate_output=lambda value: isinstance(value, str),
    )

    assert first == second == "cached"
    assert calls == 1
