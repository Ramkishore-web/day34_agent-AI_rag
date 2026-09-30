from datetime import datetime

from memory.storage import MemoryStorage


class ConversationMemory:

    def __init__(
        self,
        conversation_id,
        user_id,
        window_size=10
    ):

        self.conversation_id = conversation_id
        self.user_id = user_id
        self.window_size = window_size

        self.storage = MemoryStorage()

    def add_user_message(self, message):

        self.storage.add_message(
            conversation_id=self.conversation_id,
            user_id=self.user_id,
            role="user",
            message=message,
            timestamp=datetime.now().isoformat()
        )

    def add_assistant_message(self, message):

        self.storage.add_message(
            conversation_id=self.conversation_id,
            user_id=self.user_id,
            role="assistant",
            message=message,
            timestamp=datetime.now().isoformat()
        )

    def get_recent_messages(self):

        messages = self.storage.get_conversation(
            self.conversation_id,
            self.user_id
        )

        return messages[-self.window_size:]

    def clear_memory(self):

        messages = self.storage._load()

        remaining = [
            item
            for item in messages
            if not (
                item["conversation_id"]
                == self.conversation_id
                and item["user_id"]
                == self.user_id
            )
        ]

        self.storage._save(remaining)


if __name__ == "__main__":

    memory = ConversationMemory(
        conversation_id="conv-001",
        user_id="user-001",
        window_size=10
    )

    memory.add_user_message(
        "What is the leave policy?"
    )

    memory.add_assistant_message(
        "Please refer to the company leave policy."
    )

    memory.add_user_message(
        "What about carry-forward?"
    )

    print("\nRecent Conversation:")

    for message in memory.get_recent_messages():

        print(
            message["role"],
            ":",
            message["message"]
        )

        print(
            "Timestamp:",
            message["timestamp"]
        )
