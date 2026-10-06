from typing import Any

from src.tools.registry import tool_registry
from src.orchestration.retry_executor import RetryExecutor


class ToolExecutor:
    """
    Executes tools through the central Tool Registry
    with retry and error recovery support.
    """

    def __init__(self, max_retries: int = 2):
        self.retry_executor = RetryExecutor(
            max_retries=max_retries
        )

    def execute(
        self,
        tool_name: str,
        **kwargs
    ) -> Any:
        """
        Execute a registered tool with retry support.
        """

        print(
            f"[Tool Executor] Calling tool: {tool_name}"
        )

        def operation():

            return tool_registry.execute(
                tool_name,
                **kwargs
            )

        result = self.retry_executor.execute(
            operation
        )

        if result["success"]:

            print(
                f"[Tool Executor] Tool completed: "
                f"{tool_name}"
            )

            return {
                "success": True,
                "tool": tool_name,
                "result": result["result"],
                "attempts": result["attempts"]
            }

        print(
            f"[Tool Executor] Tool failed after "
            f"{result['attempts']} attempts: "
            f"{tool_name}"
        )

        return {
            "success": False,
            "tool": tool_name,
            "error": result["error"],
            "attempts": result["attempts"]
        }


def create_tool_executor() -> ToolExecutor:
    return ToolExecutor()