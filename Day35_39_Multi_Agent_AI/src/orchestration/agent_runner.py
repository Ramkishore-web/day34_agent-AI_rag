from typing import Callable, Optional

from src.memory.state import AgentState
from src.orchestration.execution_tracker import ExecutionTracker


class AgentRunner:
    """
    Executes an agent with retry and error handling.
    """

    def __init__(
        self,
        max_attempts: int = 3,
        execution_tracker: Optional[
            ExecutionTracker
        ] = None
    ):

        self.max_attempts = max_attempts

        self.execution_tracker = (
            execution_tracker
            if execution_tracker is not None
            else ExecutionTracker()
        )

    def run(
        self,
        state: AgentState,
        agent_name: str,
        operation: Callable[
            [AgentState],
            AgentState
        ]
    ) -> AgentState:

        tracker_event = (
            self.execution_tracker.start_agent(
                agent_name
            )
        )

        start_time = tracker_event["start_time"]

        for attempt in range(
            1,
            self.max_attempts + 1
        ):

            print(
                f"[AgentRunner] "
                f"{agent_name} "
                f"attempt {attempt}/"
                f"{self.max_attempts}"
            )

            state.current_agent = agent_name

            try:

                result = operation(state)

                self.execution_tracker.complete_agent(
                    agent_name,
                    start_time
                )

                print(
                    f"[AgentRunner] "
                    f"{agent_name} completed."
                )

                return result

            except Exception as exc:

                error_message = str(exc)

                self.execution_tracker.fail_agent(
                    agent_name,
                    error_message,
                    attempt
                )

                state.errors.append({
                    "agent": agent_name,
                    "message": error_message,
                    "attempt": attempt,
                    "max_attempts": self.max_attempts
                })

                print(
                    f"[AgentRunner] "
                    f"{agent_name} failed "
                    f"on attempt {attempt}: "
                    f"{error_message}"
                )

                if attempt < self.max_attempts:

                    print(
                        f"[AgentRunner] "
                        f"Retrying {agent_name}..."
                    )

                    continue

                state.task_status = "agent_failed"

                return state

        state.task_status = "agent_failed"

        return state


def create_agent_runner(
    max_attempts: int = 3
) -> AgentRunner:

    return AgentRunner(
        max_attempts=max_attempts
    )