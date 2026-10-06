from typing import List, Dict


class Retriever:
    """
    Simple document retriever for the Day 35-39 Multi-Agent AI system.
    """

    def __init__(self):
        self.documents = [
            {
                "source": "leave_policy.txt",
                "content": (
                    "Employees are eligible for leave according to "
                    "company leave rules and approval procedures."
                ),
            },
            {
                "source": "salary_policy.txt",
                "content": (
                    "Employee salary is processed according to the "
                    "company payroll policy and applicable attendance records."
                ),
            },
            {
                "source": "attendance_policy.txt",
                "content": (
                    "Employee attendance is recorded according to "
                    "company attendance rules. Attendance information "
                    "may be considered during payroll processing."
                ),
            },
        ]

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> List[Dict]:
        """
        Retrieve relevant documents based on simple keyword matching.
        """

        query_words = set(query.lower().split())

        scored_documents = []

        for document in self.documents:
            content = document["content"].lower()

            score = sum(
                1
                for word in query_words
                if len(word) > 2 and word in content
            )

            scored_documents.append(
                {
                    "source": document["source"],
                    "content": document["content"],
                    "score": score,
                }
            )

        scored_documents.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return scored_documents[:top_k]


def create_retriever() -> Retriever:
    """Create and return a Retriever."""
    return Retriever()