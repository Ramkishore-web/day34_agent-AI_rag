import asyncio
from typing import Any, Awaitable, Callable

from src.orchestration.retry_executor import RetryExecutor


class ResilientExecutor:
    """
    Executes an async operation with:
    1. Timeout protection
    2. Retry support
    """

    def __init__(
        self,
        timeout_seconds: float = 5.0,
        max_retries: int = 2
    ):
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries

    async def execute(
        self,
        operation: Callable[[], Awaitable[Any]]
    ) -> dict:

        attempts = 0
        last_error = None

        while attempts <= self.max_retries:

            attempts += 1

            try:

                result = await asyncio.wait_for(
                    operation(),
                    timeout=self.timeout_seconds
                )

                return {
                    "success": True,
                    "result": result,
                    "attempts": attempts,
                    "timed_out": False
                }

            except asyncio.TimeoutError:

                last_error = (
                    f"Operation exceeded "
                    f"{self.timeout_seconds} seconds."
                )

                print(
                    f"[ResilientExecutor] "
                    f"Attempt {attempts} timed out."
                )

            except Exception as exc:

                last_error = str(exc)

                print(
                    f"[ResilientExecutor] "
                    f"Attempt {attempts} failed: {exc}"
                )

        return {
            "success": False,
            "result": None,
            "attempts": attempts,
            "timed_out": True,
            "error": last_error
        }


def create_resilient_executor(
    timeout_seconds: float = 5.0,
    max_retries: int = 2
) -> ResilientExecutor:

    return ResilientExecutor(
        timeout_seconds=timeout_seconds,
        max_retries=max_retries
    )