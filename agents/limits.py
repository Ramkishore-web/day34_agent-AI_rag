import time


MAX_ITERATIONS = 5
MAX_TOOL_CALLS = 10
MAX_RUNTIME_SECONDS = 30


class AgentExecutionLimits:

    def __init__(self):

        self.iterations = 0
        self.tool_calls = 0
        self.start_time = time.time()

    def can_continue(self):

        elapsed_time = time.time() - self.start_time

        if self.iterations >= MAX_ITERATIONS:
            return False, "Maximum iterations reached."

        if self.tool_calls >= MAX_TOOL_CALLS:
            return False, "Maximum tool calls reached."

        if elapsed_time >= MAX_RUNTIME_SECONDS:
            return False, "Maximum runtime reached."

        return True, "Execution allowed."

    def next_iteration(self):

        self.iterations += 1

    def record_tool_call(self):

        self.tool_calls += 1

    def elapsed_seconds(self):

        return round(
            time.time() - self.start_time,
            3
        )


if __name__ == "__main__":

    limits = AgentExecutionLimits()

    print("Maximum Iterations:", MAX_ITERATIONS)
    print("Maximum Tool Calls:", MAX_TOOL_CALLS)
    print("Maximum Runtime:", MAX_RUNTIME_SECONDS, "seconds")

    for i in range(7):

        allowed, message = limits.can_continue()

        print(
            f"\nIteration {i + 1}:",
            message
        )

        if not allowed:

            print(
                "Unable to complete the operation "
                "within the allowed execution limits."
            )

            break

        limits.next_iteration()
        limits.record_tool_call()

        print(
            "Tool calls:",
            limits.tool_calls
        )
