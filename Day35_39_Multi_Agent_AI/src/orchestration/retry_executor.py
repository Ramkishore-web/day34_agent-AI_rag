from typing import Callable, Any


class RetryExecutor:
    """
    Executes an operation with retry support.
    """

    def __init__(self, max_retries: int = 2):
        self.max_retries = max_retries

    def execute(
        self,
        operation: Callable[[], Any]
    ) -> dict:
        """
        Execute an operation and retry if it fails.
        """

        attempts = 0
        last_error = None

        while attempts <= self.max_retries:

            attempts += 1

            try:

                result = operation()

                return {
                    "success": True,
                    "result": result,
                    "attempts": attempts
                }

            except Exception as exc:

                last_error = str(exc)

                print(
                    f"[RetryExecutor] "
                    f"Attempt {attempts} failed: {exc}"
                )

        return {
            "success": False,
            "error": last_error,
            "attempts": attempts
        }


def create_retry_executor() -> RetryExecutor:
    return RetryExecutor()