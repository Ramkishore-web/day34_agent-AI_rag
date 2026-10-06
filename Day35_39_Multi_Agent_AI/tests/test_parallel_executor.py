import asyncio

from src.orchestration.parallel_executor import (
    ParallelExecutor
)


async def task_one():
    await asyncio.sleep(0.1)
    return "Research completed"


async def task_two():
    await asyncio.sleep(0.1)
    return "RAG completed"


def test_parallel_executor():

    executor = ParallelExecutor()

    results = asyncio.run(
        executor.run(
            task_one,
            task_two
        )
    )

    assert len(results) == 2
    assert results[0] == "Research completed"
    assert results[1] == "RAG completed"