from calculator_tool import CalculatorTool
from rag_tool import RAGTool


class Executor:

    def __init__(self):

        self.calculator = CalculatorTool()
        self.rag = RAGTool()

    def select_tool(self, task):

        task_lower = task.lower()

        if any(word in task_lower for word in [
            "calculate",
            "add",
            "subtract",
            "multiply",
            "divide"
        ]):
            return "calculator"

        if any(word in task_lower for word in [
            "customer",
            "invoice",
            "product",
            "quantity",
            "price",
            "total",
            "policy"
        ]):
            return "rag"

        return None

    def execute(self, task):

        tool_name = self.select_tool(task)

        print("\nTask:", task)
        print("Selected Tool:", tool_name)

        if tool_name == "rag":

            results = self.rag.search(
                task,
                top_k=2
            )

            return {
                "task": task,
                "tool": tool_name,
                "result": results
            }

        if tool_name == "calculator":

            return {
                "task": task,
                "tool": tool_name,
                "result": "Calculator task detected."
            }

        return {
            "task": task,
            "tool": None,
            "result": "No suitable tool found."
        }


if __name__ == "__main__":

    executor = Executor()

    tasks = [
        "Find customer information",
        "Find total invoice amount"
    ]

    print("\n========== EXECUTOR ==========")

    for task in tasks:

        result = executor.execute(task)

        print("Execution Result:")

        if isinstance(result["result"], list):

            for item in result["result"]:

                print(
                    item["document"]
                )

        else:

            print(
                result["result"]
            )
