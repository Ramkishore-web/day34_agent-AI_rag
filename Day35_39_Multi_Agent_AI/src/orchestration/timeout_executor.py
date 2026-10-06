import asyncio
from typing import Any, Awaitable, Callable


class TimeoutExecutor:
    """
    Executes an async operation with a timeout.
    """

    def __init__(self, timeout_seconds: float = 5.0):
        self.timeout_seconds = timeout_seconds

    async def execute(
        self,
        operation: Callable[[], Awaitable[Any]]
    ) -> dict:
        """
        Execute an async operation with timeout protection.
        """

        try:

            result = await asyncio.wait_for(
                operation(),
                timeout=self.timeout_seconds
            )

            return {
                "success": True,
                "result": result,
                "timed_out": False
            }

        except asyncio.TimeoutError:

            print(
                "[TimeoutExecutor] Operation timed out."
            )

            return {
                "success": False,
                "result": None,
                "timed_out": True,
                "error": (
                    f"Operation exceeded "
                    f"{self.timeout_seconds} seconds."
                )
            }

        except Exception as exc:

            return {
                "success": False,
                "result": None,
                "timed_out": False,
                "error": str(exc)
            }


def create_timeout_executor(
    timeout_seconds: float = 5.0
) -> TimeoutExecutor:

    return TimeoutExecutor(
        timeout_seconds=timeout_seconds
    )