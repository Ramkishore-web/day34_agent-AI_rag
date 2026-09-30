from planner import Planner
from tool_registry import ToolRegistry
from state import AgentState


class AgentWorkflow:

    def __init__(self):

        print("Starting Agent Workflow...")

        self.planner = Planner()
        self.registry = ToolRegistry()

    def select_tool(self, task):

        task_lower = task.lower()

        if "customer" in task_lower:
            return "rag"

        if "total amount" in task_lower:
            return "rag"

        if "invoice" in task_lower:
            return "rag"

        if "product" in task_lower:
            return "rag"

        if "quantity" in task_lower:
            return "rag"

        if "price" in task_lower:
            return "rag"

        if "calculate" in task_lower:
            return "calculator"

        return None

    def execute_tool(self, tool_name, task):

        tool = self.registry.get_tool(tool_name)

        if tool is None:
            return "Tool not found."

        if tool_name == "rag":

            return tool.search(
                task,
                top_k=2
            )

        if tool_name == "calculator":

            return "Calculator execution requires numeric arguments."

        return "Tool execution not implemented."

    def create_final_answer(self, state):

        answers = []

        for result in state.tool_results:

            if isinstance(result, list):

                for item in result:

                    document = item.get(
                        "document",
                        ""
                    )

                    if document:
                        answers.append(document)

            else:

                answers.append(str(result))

        if not answers:

            return "No relevant information was found."

        return "\n".join(answers)

    def run(self, question):

        print("\n========================================")
        print("AGENT WORKFLOW STARTED")
        print("========================================")

        # 1. Create state
        state = AgentState(question)

        print("\n1. State created")

        # 2. Create plan
        state.plan = self.planner.create_plan(
            question
        )

        print("\n2. Plan created")

        for number, task in enumerate(
            state.plan,
            start=1
        ):
            print(f"Task {number}: {task}")

        # 3. Execute planned tasks
        print("\n3. Executing workflow")

        for task in state.plan:

            print("\nTask:", task)

            tool_name = self.select_tool(task)

            print("Selected Tool:", tool_name)

            if tool_name is None:

                print("No suitable tool found.")
                continue

            result = self.execute_tool(
                tool_name,
                task
            )

            state.add_tool_result(result)

            if isinstance(result, list):

                for item in result:

                    document = item.get(
                        "document",
                        ""
                    )

                    if document:
                        state.add_document(
                            document
                        )

            print("Tool execution completed.")

        # 4. Generate final answer
        print("\n4. Creating final answer")

        final_answer = self.create_final_answer(
            state
        )

        state.set_final_answer(
            final_answer
        )

        # 5. Display state
        state.show_state()

        print("\n========================================")
        print("WORKFLOW COMPLETED")
        print("========================================")


workflow = AgentWorkflow()

workflow.run(
    "Find the customer and tell me the total amount."
)
