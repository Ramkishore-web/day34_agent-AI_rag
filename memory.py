class ConversationMemory:

    def __init__(self):
        self.messages = []

    def add_message(self, role, content):

        self.messages.append(
            {
                "role": role,
                "content": content
            }
        )

    def get_messages(self):

        return self.messages

    def get_last_message(self):

        if not self.messages:
            return None

        return self.messages[-1]

    def clear(self):

        self.messages = []


if __name__ == "__main__":

    memory = ConversationMemory()

    memory.add_message(
        "user",
        "My name is Ram Kishore."
    )

    memory.add_message(
        "assistant",
        "Nice to meet you, Ram Kishore."
    )

    print("Conversation Memory:")

    for message in memory.get_messages():
        print(message["role"], ":", message["content"])
