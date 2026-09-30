class Planner:

    def create_plan(self, question):

        question_lower = question.lower()

        tasks = []

        if "customer" in question_lower:
            tasks.append("Find customer information")

        if "total amount" in question_lower:
            tasks.append("Find total invoice amount")

        if "invoice" in question_lower:
            if "total amount" not in question_lower:
                tasks.append("Find invoice information")

        if "product" in question_lower:
            tasks.append("Find product information")

        if "quantity" in question_lower:
            tasks.append("Find quantity information")

        if "price" in question_lower:
            tasks.append("Find price information")

        if not tasks:
            tasks.append("Process the question as a general request")

        return tasks


if __name__ == "__main__":

    planner = Planner()

    question = "Find the customer and tell me the total amount."

    plan = planner.create_plan(question)

    print("User Question:")
    print(question)

    print("\nAgent Plan:")

    for number, task in enumerate(plan, start=1):
        print(f"Task {number}: {task}")
