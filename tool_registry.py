from calculator_tool import CalculatorTool
from company_info_tool import CompanyInfoTool
from rag_tool import RAGTool


class ToolRegistry:

    def __init__(self):

        print("Initializing Tool Registry...")

        self.calculator = CalculatorTool()
        self.company_info = CompanyInfoTool()
        self.rag = RAGTool()

        self.tools = {
            "calculator": self.calculator,
            "company_info": self.company_info,
            "rag": self.rag
        }

    def get_tool(self, tool_name):

        return self.tools.get(tool_name)

    def list_tools(self):

        return list(self.tools.keys())


if __name__ == "__main__":

    registry = ToolRegistry()

    print("\nAvailable Tools:")

    for tool in registry.list_tools():
        print("-", tool)
