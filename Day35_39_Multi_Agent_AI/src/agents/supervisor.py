from src.memory.state import AgentState


class SupervisorAgent:
    """
    Supervisor controls the flow of the multi-agent system
    and decides whether a tool is required.
    """

    def __init__(self):
        self.name = "Supervisor"

    def requires_tool(self, request: str) -> bool:
        """
        Determine whether the user request requires a tool.
        """

        request = request.lower().strip()

        tool_keywords = [
            "calculate",
            "percentage",
            "percent",
            "multiply",
            "divide",
            "sum",
            "subtract",
            "search document",
            "read document",
            "validate"
        ]

        return any(
            keyword in request
            for keyword in tool_keywords
        )

    def decide_tool(self, request: str) -> str:
        """
        Decide which category of tool is required.
        """

        request = request.lower().strip()

        if any(word in request for word in [
            "calculate",
            "percentage",
            "percent",
            "multiply",
            "divide",
            "sum",
            "subtract"
        ]):
            return "calculator"

        if "read document" in request:
            return "document_reader"

        if "search document" in request:
            return "document_search"

        if "validate" in request:
            return "validation_tool"

        return "rag_search"

    def decide_next_agent(self, state: AgentState) -> str:
        """
        Decide which agent should handle the next step.
        """

        if not state.research_results:
            return "researcher"

        if not state.retrieved_documents:
            return "rag"

        if not state.analysis_results:
            return "analyst"

        if not state.validation_results:
            return "validator"

        if not state.final_response:
            return "writer"

        return "completed"


def create_supervisor() -> SupervisorAgent:
    """Create and return a Supervisor Agent."""
    return SupervisorAgent()