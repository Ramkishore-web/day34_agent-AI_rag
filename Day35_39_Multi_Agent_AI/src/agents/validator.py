from src.memory.state import AgentState


class ValidatorAgent:
    """
    Validator Agent checks whether the previous
    agent results are available and usable.
    """

    def __init__(self):
        self.name = "Validator"

    def validate(self, state: AgentState) -> AgentState:
        """
        Validate research, retrieval, and analysis results.
        """

        state.current_agent = self.name
        state.task_status = "validating"

        checks = {
            "research_available": len(state.research_results) > 0,
            "documents_available": len(state.retrieved_documents) > 0,
            "analysis_available": len(state.analysis_results) > 0,
        }

        is_valid = all(checks.values())

        result = {
            "checks": checks,
            "is_valid": is_valid,
            "message": (
                "Validation successful."
                if is_valid
                else "Validation failed. Required results are missing."
            ),
        }

        state.validation_results.append(result)

        if is_valid:
            state.task_status = "validation_completed"
        else:
            state.task_status = "validation_failed"

        return state


def create_validator() -> ValidatorAgent:
    """Create and return a Validator Agent."""
    return ValidatorAgent()