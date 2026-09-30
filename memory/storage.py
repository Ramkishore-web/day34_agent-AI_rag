import json
from pathlib import Path


class MemoryStorage:

    def __init__(self, file_path="outputs/conversations.json"):

        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.file_path.exists():

            self.file_path.write_text(
                "[]",
                encoding="utf-8"
            )

    def _load(self):

        try:

            return json.loads(
                self.file_path.read_text(
                    encoding="utf-8"
                )
            )

        except (json.JSONDecodeError, OSError):

            return []

    def _save(self, conversations):

        self.file_path.write_text(
            json.dumps(
                conversations,
                indent=4
            ),
            encoding="utf-8"
        )

    def add_message(
        self,
        conversation_id,
        user_id,
        role,
        message,
        timestamp
    ):

        conversations = self._load()

        conversations.append(
            {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "role": role,
                "message": message,
                "timestamp": timestamp
            }
        )

        self._save(conversations)

    def get_conversation(
        self,
        conversation_id,
        user_id
    ):

        conversations = self._load()

        return [
            item
            for item in conversations
            if (
                item["conversation_id"] == conversation_id
                and item["user_id"] == user_id
            )
        ]
