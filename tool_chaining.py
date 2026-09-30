from calculator_tool import CalculatorTool
from rag_tool import RAGTool


class ToolChainingAgent:

    def __init__(self):

        print("Initializing Tool Chaining Agent...")

        self.rag = RAGTool()
        self.calculator = CalculatorTool()

    def search_product_information(self):

        print("\nSTEP 1: Calling RAG Tool")

        results = self.rag.search(
            "What is the product price and quantity?",
            top_k=3
        )

        for result in results:

            document = result.get(
                "document",
                ""
            )

            print("Retrieved:", document)

        return results

    def extract_values(self, results):

        price = None
        quantity = None

        for result in results:

            document = result.get(
                "document",
                ""
            )

            if "Price:" in document:

                try:
                    price_text = document.split(
                        "Price:"
                    )[1].strip()

                    price = float(
                        price_text.split(".")[0]
                    )

                except (ValueError, IndexError):
                    pass

            if "Quantity:" in document:

                try:
                    quantity_text = document.split(
                        "Quantity:"
                    )[1]

                    quantity = float(
                        quantity_text.split(".")[0]
                    )

                except (ValueError, IndexError):
                    pass

        return price, quantity

    def run(self):

        print("\n======================================")
        print("TOOL CHAINING STARTED")
        print("======================================")

        # Tool 1: RAG
        results = self.search_product_information()

        # Extract values from RAG result
        price, quantity = self.extract_values(
            results
        )

        print("\nExtracted Price:", price)
        print("Extracted Quantity:", quantity)

        if price is None or quantity is None:

            print(
                "\nCould not extract price or quantity."
            )

            return

        # Tool 2: Calculator
        print("\nSTEP 2: Calling Calculator Tool")

        total = self.calculator.multiply(
            price,
            quantity
        )

        print("Calculated Total:", total)

        print("\nSTEP 3: Final Result")

        print(
            f"Price = {price}, "
            f"Quantity = {quantity}, "
            f"Total = {total}"
        )

        print("\n======================================")
        print("TOOL CHAINING COMPLETED")
        print("======================================")


if __name__ == "__main__":

    agent = ToolChainingAgent()

    agent.run()
