from src.memory.state import AgentState
from src.agents.aggregator import AggregatorAgent


def test_aggregator():

    state = AgentState(
        conversation_id="test-123",
        user_request="What is the leave policy?"
    )

    state.research_results.append({
        "source": "research",
        "summary": "Research completed."
    })

    state.retrieved_documents.append({
        "source": "leave_policy.txt",
        "content": "Employees can apply for leave."
    })

    agent = AggregatorAgent()

    result = agent.aggregate(state)

    assert result.current_agent == "Aggregator"

    assert result.task_status == "aggregation_completed"

    assert len(result.analysis_results) == 1

    aggregated = result.analysis_results[0]

    assert aggregated["research_count"] == 1

    assert aggregated["document_count"] == 1