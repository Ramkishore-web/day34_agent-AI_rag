from src.memory.state import AgentState


class AggregatorAgent:
    """
    Aggregator Agent combines Researcher and RAG results
    and detects possible conflicts.
    """

    def __init__(self):
        self.name = "Aggregator"

    def aggregate(self, state: AgentState) -> AgentState:

        state.current_agent = self.name
        state.task_status = "aggregating"

        research_data = state.research_results
        retrieved_data = state.retrieved_documents

        # -------------------------------------------------
        # Conflict Detection
        # -------------------------------------------------

        conflicts = []

        if research_data and retrieved_data:

            research_text = " ".join(
                str(item)
                for item in research_data
            ).lower()

            document_text = " ".join(
                str(item)
                for item in retrieved_data
            ).lower()

            # Basic contradiction detection
            if (
                "not allowed" in research_text
                and "allowed" in document_text
            ):
                conflicts.append({
                    "type": "contradiction",
                    "message": (
                        "Researcher and RAG results "
                        "may contain conflicting information."
                    )
                })

            if (
                "allowed" in research_text
                and "not allowed" in document_text
            ):
                conflicts.append({
                    "type": "contradiction",
                    "message": (
                        "Researcher and RAG results "
                        "may contain conflicting information."
                    )
                })

        # -------------------------------------------------
        # Aggregated Result
        # -------------------------------------------------

        aggregated_result = {
            "agent": self.name,
            "research_results": research_data,
            "retrieved_documents": retrieved_data,
            "research_count": len(research_data),
            "document_count": len(retrieved_data),
            "conflicts": conflicts,
            "has_conflicts": len(conflicts) > 0,
            "summary": (
                "Research and RAG results aggregated successfully."
            ),
        }

        state.analysis_results.append(
            aggregated_result
        )

        if conflicts:

            state.errors.append({
                "agent": self.name,
                "message": (
                    "Potential conflict detected "
                    "between agent results."
                ),
                "conflicts": conflicts
            })

        state.task_status = "aggregation_completed"

        return state


def create_aggregator() -> AggregatorAgent:
    """Create and return an Aggregator Agent."""
    return AggregatorAgent()