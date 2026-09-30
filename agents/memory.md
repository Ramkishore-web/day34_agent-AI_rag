# Agent Memory

## 1. Short-Term Memory

Short-term memory stores recent conversation information that the Agent needs during the current interaction.

Example:

User:
"My name is Ravi."

Agent:
"Nice to meet you, Ravi."

User:
"What is my name?"

Agent:
"Your name is Ravi."

---

## 2. Long-Term Memory

Long-term memory stores information that may be useful across conversations or sessions.

Examples:

- User preferences
- Important user information
- Previous interactions
- Persistent application information

---

## 3. Conversation History

Conversation history contains previous messages exchanged between the user and the Agent.

Example:

USER:
What is the leave policy?

ASSISTANT:
Employees receive information according to the company leave policy.

USER:
What about carry-forward?

The Agent should use the previous conversation context to understand that "carry-forward" refers to the leave policy.

---

## 4. Working Memory

Working memory contains information currently needed to complete the Agent's task.

Example:

User Request:
"Find the customer and total invoice amount."

Working Memory:

- Customer task
- Invoice task
- Retrieved documents
- Tool results

---

## 5. User Preferences

An Agent may store user preferences that help provide consistent responses.

Examples:

- Preferred response format
- Preferred language
- Preferred report structure

---

## 6. Memory Architecture

User
?
Agent
?
Memory Manager
?
Relevant Memory
?
Agent
?
Tool / RAG
?
Final Answer

---

## 7. Important Principle

Memory is application state.

Memory should not automatically be treated as permanent truth.

The application should decide what information is stored, how long it is retained, and when it should be used.

---

## 8. Summary

Short-Term Memory
? Recent conversation context

Long-Term Memory
? Information that may persist across sessions

Conversation History
? Previous user and assistant messages

Working Memory
? Information needed for the current task

User Preferences
? Stored preferences used for consistent interactions
