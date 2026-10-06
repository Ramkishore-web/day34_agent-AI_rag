from src.memory.state import AgentState
from src.orchestration.agent_runner import AgentRunner


def create_state():

    return AgentState(
        conversation_id="test-conversation",
        user_request="Test request"
    )


def test_agent_runner_success():

    state = create_state()

    runner = AgentRunner(max_attempts=3)

    def successful_agent(state):

        state.task_status = "success"
        return state

    result = runner.run(
        state,
        "TestAgent",
        successful_agent
    )

    assert result.task_status == "success"
    assert len(result.errors) == 0


def test_agent_runner_failure():

    state = create_state()

    runner = AgentRunner(max_attempts=3)

    def failing_agent(state):

        raise ValueError("Agent failed")

    result = runner.run(
        state,
        "TestAgent",
        failing_agent
    )

    assert result.task_status == "agent_failed"
    assert len(result.errors) == 3
    assert result.errors[-1]["agent"] == "TestAgent"