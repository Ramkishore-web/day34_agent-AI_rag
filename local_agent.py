from calculator_tool import CalculatorTool
from rag_tool import RAGTool


class LocalAgent:

    def __init__(self):
        print("Initializing Local Agent...")

        self.calculator = CalculatorTool()
        self.rag = RAGTool()

    def choose_tool(self, question):

        q = question.lower()

        if any(word in q for word in [
            "calculate",
            "add",
            "subtract",
            "multiply",
            "divide"
        ]):
            return "calculator"

        if any(word in q for word in [
            "customer",
            "invoice",
            "product",
            "quantity",
            "price",
            "total amount"
        ]):
            return "rag"

        return "none"

    def run(self, question):

        print("\n===================================")
        print("USER:", question)

        tool_name = self.choose_tool(question)

        print("SELECTED TOOL:", tool_name)

        if tool_name == "rag":

            results = self.rag.search(
                question,
                top_k=2
            )

            print("\nRAG RESULTS:")

            if not results:
                print("No relevant information found.")
                return

            for result in results:

                print("\nDocument:")
                print(result["document"])

                print("Distance:")
                print(result["distance"])

        elif tool_name == "calculator":

            q = question.lower()

            if "multiply" in q:
                result = self.calculator.multiply(
                    80000,
                    2
                )

            elif "add" in q:
                result = self.calculator.add(
                    100,
                    50
                )

            elif "subtract" in q:
                result = self.calculator.subtract(
                    100,
                    50
                )

            elif "divide" in q:
                result = self.calculator.divide(
                    100,
                    5
                )

            else:
                result = "Calculation not recognized."

            print("\nCALCULATOR RESULT:")
            print(result)

        else:
            print("\nNo suitable tool found.")


if __name__ == "__main__":

    agent = LocalAgent()

    agent.run("Who is the customer?")

    agent.run("What is the total amount?")

    agent.run("What product was purchased?")

    agent.run("Multiply 80000 by 2")
