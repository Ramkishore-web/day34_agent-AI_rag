from src.agents.supervisor import SupervisorAgent


supervisor = SupervisorAgent()


questions = [
    "Calculate 1000 * 18 / 100",
    "Search document salary_policy.txt",
    "Read document attendance_policy.txt",
    "Validate this answer",
    "How does the company leave policy work?"
]


for question in questions:

    print("\n" + "=" * 60)
    print("REQUEST:", question)

    requires_tool = supervisor.requires_tool(question)

    print("REQUIRES TOOL:", requires_tool)

    if requires_tool:
        tool = supervisor.decide_tool(question)
        print("SELECTED TOOL:", tool)