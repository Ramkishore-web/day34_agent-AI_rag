from src.tools.selector import ToolSelector
from src.tools.executor import ToolExecutor


selector = ToolSelector()
executor = ToolExecutor()


questions = [
    "Calculate 1000 * 18 / 100",
    "How does the company leave policy work?",
    "Search document salary_policy.txt",
    "Read document attendance_policy.txt",
    "Validate this answer"
]


for question in questions:

    print("\n" + "=" * 60)
    print(f"USER REQUEST: {question}")

    # Step 1: Select tool
    tool_name = selector.select(question)

    print(f"SELECTED TOOL: {tool_name}")

    # Step 2: Prepare arguments
    if tool_name == "calculator":

        result = executor.execute(
            tool_name,
            expression="1000 * 18 / 100"
        )

    elif tool_name == "document_reader":

        result = executor.execute(
            tool_name,
            document_name="attendance_policy.txt"
        )

    elif tool_name == "validation_tool":

        result = executor.execute(
            tool_name,
            data={
                "answer": "Test answer"
            }
        )

    else:

        result = executor.execute(
            tool_name,
            query=question
        )

    print("TOOL RESULT:")
    print(result)