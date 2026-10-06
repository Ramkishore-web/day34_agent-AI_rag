class ToolSelector:
    """
    Selects the appropriate tool based on the user request.
    """

    def select(self, request: str) -> str:

        request = request.lower().strip()

        # -------------------------------------------------
        # 1. Document reader
        # -------------------------------------------------
        if "read document" in request:
            return "document_reader"

        # -------------------------------------------------
        # 2. Document search
        # -------------------------------------------------
        if "search document" in request:
            return "document_search"

        # -------------------------------------------------
        # 3. Calculator
        # -------------------------------------------------
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

        # -------------------------------------------------
        # 4. RAG search
        # -------------------------------------------------
        if any(word in request for word in [
            "leave",
            "salary",
            "attendance",
            "policy",
            "company",
            "employee"
        ]):
            return "rag_search"

        # -------------------------------------------------
        # 5. Validation
        # -------------------------------------------------
        if "validate" in request:
            return "validation_tool"

        # -------------------------------------------------
        # 6. Default
        # -------------------------------------------------
        return "document_search"


def create_tool_selector():
    return ToolSelector()