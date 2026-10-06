from src.memory.state import AgentState
from src.retrieval.retriever import create_retriever


class RAGAgent:
    """
    RAG Agent responsible for retrieving relevant
    document information for the user request.
    """

    def __init__(self):
        self.name = "RAG"
        self.retriever = create_retriever()

    def retrieve(self, state: AgentState) -> AgentState:
        """
        Retrieve relevant documents and store them
        in the shared agent state.
        """

        state.current_agent = self.name
        state.task_status = "retrieving"

        documents = self.retriever.retrieve(
            state.user_request,
            top_k=3,
        )

        for document in documents:
            state.retrieved_documents.append(document)

        state.task_status = "retrieval_completed"

        return state


def create_rag_agent() -> RAGAgent:
    """Create and return a RAG Agent."""
    return RAGAgent()