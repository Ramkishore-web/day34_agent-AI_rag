from typing import Optional

from src.memory.state import AgentState
from src.memory.memory_store import conversation_memory


class MemoryAgent:
    """
    Manages conversation memory for the multi-agent system.
    """

    def __init__(self):
        self.name = "Memory"

    def retrieve_previous_state(
        self,
        state: AgentState
    ) -> Optional[AgentState]:
        """
        Retrieve the latest previous state for this conversation.
        """

        history = conversation_memory.get_history(
            state.conversation_id
        )

        if not history:
            return None

        return history[-1]

    def save_state(
        self,
        state: AgentState
    ) -> None:
        """
        Save the current AgentState to conversation memory.
        """

        conversation_memory.save(state)

        print(
            f"[Memory] State saved for conversation: "
            f"{state.conversation_id}"
        )

    def get_previous_response(
        self,
        state: AgentState
    ) -> Optional[str]:
        """
        Return the previous final response.
        """

        previous_state = self.retrieve_previous_state(state)

        if previous_state is None:
            return None

        return previous_state.final_response


def create_memory_agent() -> MemoryAgent:
    return MemoryAgent()