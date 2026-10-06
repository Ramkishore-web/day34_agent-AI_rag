import asyncio

from src.orchestration.resilient_executor import (
    ResilientExecutor
)


def test_resilient_executor_success():

    executor = ResilientExecutor(
        timeout_seconds=1,
        max_retries=2
    )

    async def operation():

        await asyncio.sleep(0.01)

        return "Success"

    result = asyncio.run(
        executor.execute(operation)
    )

    assert result["success"] is True
    assert result["result"] == "Success"
    assert result["attempts"] == 1
    assert result["timed_out"] is False


def test_resilient_executor_timeout():

    executor = ResilientExecutor(
        timeout_seconds=0.05,
        max_retries=2
    )

    async def slow_operation():

        await asyncio.sleep(0.2)

        return "Success"

    result = asyncio.run(
        executor.execute(slow_operation)
    )

    assert result["success"] is False
    assert result["attempts"] == 3
    assert result["timed_out"] is True
    assert result["result"] is None