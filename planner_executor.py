from planner import Planner
from executor import Executor


class PlannerExecutorAgent:

    def __init__(self):

        self.planner = Planner()
        self.executor = Executor()

    def run(self, question):

        print("\n======================================")
        print("USER GOAL")
        print("======================================")

        print(question)

        # Step 1: Planning
        plan = self.planner.create_plan(
            question
        )

        print("\n======================================")
        print("PLAN")
        print("======================================")

        for number, task in enumerate(
            plan,
            start=1
        ):

            print(
                f"Task {number}: {task}"
            )

        # Step 2: Execution
        print("\n======================================")
        print("EXECUTION")
        print("======================================")

        results = []

        for task in plan:

            result = self.executor.execute(
                task
            )

            results.append(result)

        # Step 3: Final results
        print("\n======================================")
        print("FINAL RESULTS")
        print("======================================")

        for result in results:

            print(
                "\nTask:",
                result["task"]
            )

            print(
                "Tool:",
                result["tool"]
            )

            if isinstance(
                result["result"],
                list
            ):

                for item in result["result"]:

                    print(
                        "Document:",
                        item["document"]
                    )

            else:

                print(
                    "Result:",
                    result["result"]
                )


if __name__ == "__main__":

    agent = PlannerExecutorAgent()

    agent.run(
        "Find the customer and tell me the total amount."
    )
