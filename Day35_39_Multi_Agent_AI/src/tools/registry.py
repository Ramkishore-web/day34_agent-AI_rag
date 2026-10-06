from typing import Callable, Dict, Any


class ToolRegistry:
    """
    Central registry for tools used by Multi-Agent AI system.
    """

    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register(self, name: str, function: Callable):
        """Register a tool."""
        self.tools[name] = function

    def get(self, name: str) -> Callable:
        """Get a registered tool."""
        if name not in self.tools:
            raise ValueError(f"Tool not found: {name}")

        return self.tools[name]

    def list_tools(self):
        """Return all registered tool names."""
        return list(self.tools.keys())

    def execute(self, name: str, **kwargs) -> Any:
        """Execute a registered tool."""
        tool = self.get(name)
        return tool(**kwargs)


# ---------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------

def rag_search(query: str):
    """
    Search relevant information using RAG.
    """
    return {
        "tool": "rag_search",
        "query": query,
        "result": "RAG search executed successfully."
    }


def calculator(expression: str):
    """
    Perform a basic calculation.
    """

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return {
            "tool": "calculator",
            "expression": expression,
            "result": result
        }

    except Exception as exc:
        return {
            "tool": "calculator",
            "expression": expression,
            "error": str(exc)
        }


def document_search(query: str):
    """
    Search documents.
    """

    return {
        "tool": "document_search",
        "query": query,
        "result": "Document search executed successfully."
    }


def document_reader(document_name: str):
    """
    Read a document.
    """

    return {
        "tool": "document_reader",
        "document": document_name,
        "result": "Document reader executed successfully."
    }


def validation_tool(data: Any):
    """
    Validate agent output.
    """

    if data is None:
        return {
            "valid": False,
            "message": "Validation failed: empty data."
        }

    return {
        "valid": True,
        "message": "Validation successful."
    }


# ---------------------------------------------------------
# Create registry
# ---------------------------------------------------------

tool_registry = ToolRegistry()


tool_registry.register(
    "rag_search",
    rag_search
)

tool_registry.register(
    "calculator",
    calculator
)

tool_registry.register(
    "document_search",
    document_search
)

tool_registry.register(
    "document_reader",
    document_reader
)

tool_registry.register(
    "validation_tool",
    validation_tool
)