from memory.conversation import ConversationMemory


memory = ConversationMemory(
    conversation_id="conv-window-test",
    user_id="user-001",
    window_size=10
)


for number in range(1, 13):

    memory.add_user_message(
        f"Message {number}"
    )


recent = memory.get_recent_messages()


print("Total stored messages: 12")
print("Memory window size: 10")
print("Messages provided to agent:", len(recent))

print("\nRecent messages:")

for message in recent:

    print(message["message"])
