
import asyncio
from collections.abc import Callable
from typing import Any


class ToolExecutionError(RuntimeError):
    """Base error for safe tool execution."""


class ToolTimeoutError(ToolExecutionError):
    """Raised when a tool exceeds its time limit."""


class ToolOutputError(ToolExecutionError):
    """Raised when a tool returns invalid output."""


class ToolCancelledError(ToolExecutionError):
    """Raised when tool execution is cancelled."""


# Successful results are cached for this Python process only.
_RESULT_CACHE: dict[str, Any] = {}


async def execute_tool(
    tool: Callable[[], Any],
    *,
    idempotency_key: str,
    validate_output: Callable[[Any], bool],
    timeout_seconds: float = 5.0,
    max_attempts: int = 2,
) -> Any:
    """Execute an async tool with a timeout, bounded retries,
    output validation, and sequential idempotency caching.
    """
    if not idempotency_key.strip():
        raise ValueError("idempotency_key cannot be empty")

    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")

    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    if idempotency_key in _RESULT_CACHE:
        return _RESULT_CACHE[idempotency_key]

    for attempt in range(1, max_attempts + 1):
        try:
            result = await asyncio.wait_for(
                tool(),
                timeout=timeout_seconds,
            )
        except asyncio.CancelledError:
            # Preserve cancellation so the caller can handle it.
            raise
        except TimeoutError as exc:
            if attempt == max_attempts:
                raise ToolTimeoutError(
                    f"Tool timed out after {max_attempts} attempts"
                ) from exc
            continue
        except Exception as exc:
            if attempt == max_attempts:
                raise ToolExecutionError(
                    f"Tool failed after {max_attempts} attempts"
                ) from exc
            continue

        try:
            is_valid = validate_output(result)
        except Exception as exc:
            raise ToolOutputError(
                "Tool output validation raised an error"
            ) from exc

        if is_valid is not True:
            raise ToolOutputError("Tool returned invalid output")

        # Cache only validated successful results.
        _RESULT_CACHE[idempotency_key] = result
        return result

    raise ToolExecutionError("Tool execution failed")
