import asyncio

from src.orchestration.timeout_executor import (
    TimeoutExecutor
)


def test_timeout_executor_success():

    executor = TimeoutExecutor(
        timeout_seconds=1
    )

    async def fast_operation():

        await asyncio.sleep(0.01)

        return "completed"

    result = asyncio.run(
        executor.execute(fast_operation)
    )

    assert result["success"] is True
    assert result["result"] == "completed"
    assert result["timed_out"] is False


def test_timeout_executor_timeout():

    executor = TimeoutExecutor(
        timeout_seconds=0.05
    )

    async def slow_operation():

        await asyncio.sleep(0.2)

        return "completed"

    result = asyncio.run(
        executor.execute(slow_operation)
    )

    assert result["success"] is False
    assert result["timed_out"] is True
    assert result["result"] is None
    assert "exceeded" in result["error"]