from src.tools.selector import ToolSelector


selector = ToolSelector()

questions = [
    "Calculate 1000 * 18 / 100",
    "How does the company leave policy work?",
    "Search document salary_policy.txt",
    "Read document attendance_policy.txt",
    "Validate this answer"
]

for question in questions:
    tool = selector.select(question)

    print(f"Question : {question}")
    print(f"Tool     : {tool}")
    print("-" * 60)