from memory import ConversationMemory


class MemoryAgent:

    def __init__(self):

        self.memory = ConversationMemory()

    def process(self, question):

        self.memory.add_message(
            "user",
            question
        )

        question_lower = question.lower()

        # Remember user's name
        if "my name is" in question_lower:

            name = question.split("is", 1)[1].strip()

            self.memory.add_message(
                "assistant",
                f"Nice to meet you, {name}."
            )

            return f"Nice to meet you, {name}."

        # Retrieve user's name from memory
        if "what is my name" in question_lower:

            for message in self.memory.get_messages():

                content = message["content"]

                if "My name is" in content:

                    name = content.split(
                        "My name is", 1
                    )[1].strip()

                    answer = f"Your name is {name}."

                    self.memory.add_message(
                        "assistant",
                        answer
                    )

                    return answer

            return "I don't know your name yet."

        answer = "I received your message."

        self.memory.add_message(
            "assistant",
            answer
        )

        return answer


agent = MemoryAgent()

print("\nUSER: My name is Ram Kishore.")
print("AGENT:", agent.process(
    "My name is Ram Kishore."
))

print("\nUSER: What is my name?")
print("AGENT:", agent.process(
    "What is my name?"
))

print("\nMEMORY:")

for message in agent.memory.get_messages():

    print(
        message["role"],
        ":",
        message["content"]
    )
