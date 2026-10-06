from src.memory.state import AgentState


class WriterAgent:
    """
    Writer Agent converts the internal workflow results
    into a clean user-facing response.
    """

    def __init__(self):
        self.name = "Writer"

    def write(self, state: AgentState) -> AgentState:

        state.current_agent = self.name
        state.task_status = "writing"

        question = state.user_request

        # -------------------------------------------------
        # Build answer from analysis
        # -------------------------------------------------

        if state.analysis_results:

            latest_analysis = (
                state.analysis_results[-1]
            )

            if isinstance(
                latest_analysis,
                dict
            ):

                analysis = (
                    latest_analysis.get(
                        "analysis",
                        latest_analysis.get(
                            "summary",
                            ""
                        )
                    )
                )

            else:

                analysis = str(
                    latest_analysis
                )

        else:

            analysis = ""

        # -------------------------------------------------
        # Fallback to retrieved documents
        # -------------------------------------------------

        if not analysis:

            if state.retrieved_documents:

                context_parts = []

                for document in (
                    state.retrieved_documents
                ):

                    if isinstance(
                        document,
                        dict
                    ):

                        content = document.get(
                            "content",
                            ""
                        )

                        if content:
                            context_parts.append(
                                content
                            )

                if context_parts:

                    analysis = " ".join(
                        context_parts
                    )

        # -------------------------------------------------
        # Fallback message
        # -------------------------------------------------

        if not analysis:

            analysis = (
                "I could not find enough "
                "information to answer the question."
            )

        # -------------------------------------------------
        # Clean internal workflow text
        # -------------------------------------------------

        unwanted_sections = [
            "Request:",
            "Analysis:",
            "Retrieved Context:",
            "Tool Results:",
            "Validation:",
            "Research Results:",
        ]

        for section in unwanted_sections:

            if analysis.startswith(section):

                analysis = analysis[
                    len(section):
                ].strip()

        # -------------------------------------------------
        # Final user-facing answer
        # -------------------------------------------------

        state.final_answer = (
            f"{analysis}"
        )

        state.task_status = "writing_completed"

        return state


def create_writer() -> WriterAgent:

    return WriterAgent()