
import asyncio

import pytest

from src.workflow import tool_executor as executor


@pytest.fixture(autouse=True)
def clear_result_cache():
    executor._RESULT_CACHE.clear()
    yield
    executor._RESULT_CACHE.clear()


def test_source_failure_retries_then_raises():
    calls = 0

    async def failing_source():
        nonlocal calls
        calls += 1
        raise ConnectionError("source unavailable")

    async def scenario():
        with pytest.raises(executor.ToolExecutionError, match="after 2 attempts"):
            await executor.execute_tool(
                failing_source,
                idempotency_key="source_failure_test",
                validate_output=lambda value: True,
                max_attempts=2,
            )

    asyncio.run(scenario())
    assert calls == 2


def test_timeout_retries_then_raises():
    calls = 0

    async def slow_source():
        nonlocal calls
        calls += 1
        await asyncio.sleep(0.1)
        return {"ok": True}

    async def scenario():
        with pytest.raises(executor.ToolTimeoutError):
            await executor.execute_tool(
                slow_source,
                idempotency_key="timeout_test",
                validate_output=lambda value: True,
                timeout_seconds=0.01,
                max_attempts=2,
            )

    asyncio.run(scenario())
    assert calls == 2


def test_invalid_tool_output_is_rejected():
    async def source():
        return {"unexpected": "data"}

    async def scenario():
        with pytest.raises(executor.ToolOutputError):
            await executor.execute_tool(
                source,
                idempotency_key="invalid_output_test",
                validate_output=lambda value: "answer" in value,
            )

    asyncio.run(scenario())


def test_successful_result_is_cached():
    calls = 0

    async def source():
        nonlocal calls
        calls += 1
        return {"answer": "Python testing"}

    async def scenario():
        first = await executor.execute_tool(
            source,
            idempotency_key="cache_test",
            validate_output=lambda value: "answer" in value,
        )
        second = await executor.execute_tool(
            source,
            idempotency_key="cache_test",
            validate_output=lambda value: "answer" in value,
        )

        assert first == second
        assert calls == 1

    asyncio.run(scenario())


def test_invalid_configuration_is_rejected():
    async def source():
        return {"ok": True}

    async def scenario():
        with pytest.raises(ValueError, match="at least 1"):
            await executor.execute_tool(
                source,
                idempotency_key="invalid_attempts_test",
                validate_output=lambda value: True,
                max_attempts=0,
            )

    asyncio.run(scenario())
