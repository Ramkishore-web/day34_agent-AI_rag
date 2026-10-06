import uuid

from src.memory.state import AgentState
from src.orchestration.workflow import MultiAgentWorkflow


def main():

    question = "How does the company's leave policy affect salary and attendance?"

    state = AgentState(
        conversation_id=str(uuid.uuid4()),
        user_request=question
    )

    workflow = MultiAgentWorkflow()

    result = workflow.run(state)

    print("\n" + "=" * 60)
    print("WORKFLOW STATUS")
    print("=" * 60)

    print("Status:", result.task_status)
    print("Current Agent:", result.current_agent)

    print("\n" + "=" * 60)
    print("FINAL RESPONSE")
    print("=" * 60)

    print(result.final_response)

    print("\n" + "=" * 60)
    print("ERRORS")
    print("=" * 60)

    print(result.errors)


if __name__ == "__main__":
    main()