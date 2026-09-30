class AgentState:

    def __init__(self, question):

        self.question = question

        self.plan = []

        self.memory = []

        self.retrieved_documents = []

        self.tool_results = []

        self.final_answer = None

    def add_plan_task(self, task):

        self.plan.append(task)

    def add_memory(self, message):

        self.memory.append(message)

    def add_document(self, document):

        self.retrieved_documents.append(document)

    def add_tool_result(self, result):

        self.tool_results.append(result)

    def set_final_answer(self, answer):

        self.final_answer = answer

    def show_state(self):

        print("\n========== AGENT STATE ==========")

        print("\nQuestion:")
        print(self.question)

        print("\nPlan:")
        for task in self.plan:
            print("-", task)

        print("\nMemory:")
        for message in self.memory:
            print("-", message)

        print("\nRetrieved Documents:")
        for document in self.retrieved_documents:
            print("-", document)

        print("\nTool Results:")
        for result in self.tool_results:
            print("-", result)

        print("\nFinal Answer:")
        print(self.final_answer)


if __name__ == "__main__":

    state = AgentState(
        "Find the customer and total amount."
    )

    state.add_plan_task(
        "Find customer information"
    )

    state.add_plan_task(
        "Find total amount"
    )

    state.add_memory(
        "Previous conversation available"
    )

    state.add_document(
        "Customer: Ram Kishore"
    )

    state.add_tool_result(
        "RAG search completed"
    )

    state.set_final_answer(
        "Customer is Ram Kishore and total amount is 160000."
    )

    state.show_state()
