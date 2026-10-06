import asyncio
from typing import Any, Callable, List


class ParallelExecutor:
    """
    Executes independent async tasks in parallel.
    """

    def __init__(self, max_workers: int = 3):
        self.max_workers = max_workers

    async def run(
        self,
        *tasks: Callable
    ) -> List[Any]:
        """
        Execute multiple async tasks concurrently.

        Example:

            results = await executor.run(
                task_one,
                task_two
            )
        """

        if not tasks:
            return []

        print()
        print("=" * 60)
        print("PARALLEL EXECUTION STARTED")
        print("=" * 60)

        # -------------------------------------------------
        # Create task objects
        # -------------------------------------------------

        async_tasks = []

        for index, task in enumerate(tasks, start=1):

            print(
                f"[ParallelExecutor] "
                f"Starting task {index}"
            )

            async_tasks.append(
                asyncio.create_task(
                    task()
                )
            )

        # -------------------------------------------------
        # Execute concurrently
        # -------------------------------------------------

        results = await asyncio.gather(
            *async_tasks,
            return_exceptions=True
        )

        # -------------------------------------------------
        # Handle results
        # -------------------------------------------------

        final_results = []

        for index, result in enumerate(
            results,
            start=1
        ):

            if isinstance(
                result,
                Exception
            ):

                print(
                    f"[ParallelExecutor] "
                    f"Task {index} failed: "
                    f"{result}"
                )

            else:

                print(
                    f"[ParallelExecutor] "
                    f"Task {index} completed"
                )

            final_results.append(result)

        print()
        print("=" * 60)
        print("PARALLEL EXECUTION COMPLETED")
        print("=" * 60)

        return final_results


def create_parallel_executor(
    max_workers: int = 3
) -> ParallelExecutor:

    return ParallelExecutor(
        max_workers=max_workers
    )