import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from rag_tool import RAGTool


class DocumentSearchTool:

    def __init__(self):
        self.rag = RAGTool()

    def search(self, query, top_k=3):
        return self.rag.search(query, top_k=top_k)


if __name__ == "__main__":

    tool = DocumentSearchTool()

    results = tool.search(
        "What is the total amount?",
        top_k=3
    )

    print("\nDocument Search Results:")

    if not results:
        print("No results found.")

    for result in results:
        print("\nDocument:")
        print(result["document"])

        print("\nMetadata:")
        print(result["metadata"])

        print("\nDistance:")
        print(result["distance"])
