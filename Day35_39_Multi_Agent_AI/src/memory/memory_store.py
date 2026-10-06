from typing import Dict, List, Optional

from src.memory.state import AgentState


class ConversationMemory:
    """
    Stores AgentState objects by conversation_id.
    """

    def __init__(self):
        self._conversations: Dict[str, List[AgentState]] = {}

    def save(self, state: AgentState) -> None:
        """Save a state to conversation history."""

        conversation_id = state.conversation_id

        if conversation_id not in self._conversations:
            self._conversations[conversation_id] = []

        self._conversations[conversation_id].append(state)

    def get_history(
        self,
        conversation_id: str
    ) -> List[AgentState]:
        """Return conversation history."""

        return self._conversations.get(
            conversation_id,
            []
        )

    def get_latest(
        self,
        conversation_id: str
    ) -> Optional[AgentState]:
        """Return the latest state."""

        history = self.get_history(conversation_id)

        if not history:
            return None

        return history[-1]

    def clear(self, conversation_id: str) -> None:
        """Clear one conversation."""

        self._conversations.pop(
            conversation_id,
            None
        )

    def clear_all(self) -> None:
        """Clear all conversations."""

        self._conversations.clear()

    def conversation_count(self) -> int:
        """Return number of conversations."""

        return len(self._conversations)


# Global conversation memory
conversation_memory = ConversationMemory()