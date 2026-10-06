from src.memory.state import AgentState


class AnalystAgent:
    """
    Analyzes research, retrieved documents,
    memory context, and tool results.
    """

    def __init__(self):
        self.name = "Analyst"

    def analyze(self, state: AgentState) -> AgentState:

        state.current_agent = self.name
        state.task_status = "analyzing"

        # -------------------------------------------------
        # Basic counts
        # -------------------------------------------------

        analysis = {
            "agent": self.name,
            "research_count": len(
                state.research_results
            ),
            "retrieved_document_count": len(
                state.retrieved_documents
            ),
            "tool_result_count": len(
                state.tool_results
            ),
            "tool_results": state.tool_results,
            "summary": "Analysis completed."
        }

        # -------------------------------------------------
        # Tool analysis
        # -------------------------------------------------

        if state.tool_results:

            analysis["tool_analysis"] = (
                "The analysis includes results "
                "returned by the selected tool."
            )

            analysis["tool_details"] = []

            for tool_result in state.tool_results:

                if isinstance(tool_result, dict):

                    analysis["tool_details"].append(
                        tool_result
                    )

        # -------------------------------------------------
        # Document analysis
        # -------------------------------------------------

        if state.retrieved_documents:

            analysis["document_analysis"] = (
                "The analysis includes information "
                "retrieved from company documents."
            )

            analysis["retrieved_context"] = (
                state.retrieved_documents
            )

        else:

            analysis["retrieved_context"] = (
                "No retrieved context available."
            )

        # -------------------------------------------------
        # Research analysis
        # -------------------------------------------------

        if state.research_results:

            analysis["research_analysis"] = (
                "The analysis includes research results."
            )

            analysis["research_details"] = (
                state.research_results
            )

        # -------------------------------------------------
        # Memory / previous conversation analysis
        # -------------------------------------------------

        if state.tool_results:

            analysis["memory_context"] = (
                "Previous tool results are available "
                "through the shared conversation state."
            )

        else:

            analysis["memory_context"] = (
                "No previous tool results are available."
            )

        # -------------------------------------------------
        # Human-readable analysis
        # -------------------------------------------------

        analysis["analysis"] = self._build_analysis(
            state
        )

        # -------------------------------------------------
        # Store analysis
        # -------------------------------------------------

        state.analysis_results.append(
            analysis
        )

        state.task_status = "analysis_completed"

        return state

    def _build_analysis(
        self,
        state: AgentState
    ) -> str:
        """
        Build a concise analysis from the available
        workflow information.
        """

        parts = []

        # Tool information
        if state.tool_results:

            for tool_result in state.tool_results:

                if not isinstance(tool_result, dict):
                    continue

                tool_name = tool_result.get(
                    "tool",
                    "unknown"
                )

                result_data = tool_result.get(
                    "result"
                )

                # Calculator result
                if tool_name == "calculator":

                    if isinstance(
                        result_data,
                        dict
                    ):

                        calculation = (
                            result_data.get(
                                "result"
                            )
                        )

                        expression = (
                            result_data.get(
                                "expression"
                            )
                        )

                        if calculation is not None:

                            parts.append(
                                f"Calculation "
                                f"'{expression}' "
                                f"produced "
                                f"{calculation}."
                            )

                else:

                    parts.append(
                        f"Tool '{tool_name}' "
                        f"returned a result."
                    )

        # Documents
        if state.retrieved_documents:

            parts.append(
                f"{len(state.retrieved_documents)} "
                f"retrieved document(s) are available "
                f"for analysis."
            )

        # Research
        if state.research_results:

            parts.append(
                f"{len(state.research_results)} "
                f"research result(s) are available."
            )

        # No information
        if not parts:

            parts.append(
                "Analysis completed using the "
                "available workflow information."
            )

        return " ".join(parts)


def create_analyst() -> AnalystAgent:
    return AnalystAgent()