from src.memory.state import AgentState


class ResearchAgent:
    """
    Research Agent responsible for collecting and organizing
    initial information related to the user's request.
    """

    def __init__(self):
        self.name = "Researcher"

    def research(self, state: AgentState) -> AgentState:
        """
        Perform the initial research step.

        This is currently a simple foundation implementation.
        Real web/API research tools can be connected later.
        """

        state.current_agent = self.name
        state.task_status = "researching"

        result = {
            "source": "initial_research",
            "query": state.user_request,
            "summary": (
                f"Research initiated for: {state.user_request}"
            ),
        }

        state.research_results.append(result)

        state.task_status = "research_completed"

        return state


def create_researcher() -> ResearchAgent:
    """Create and return a Research Agent."""
    return ResearchAgent()