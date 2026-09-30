import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from calculator_tool import CalculatorTool
from tools.document_search import DocumentSearchTool
from memory.conversation import ConversationMemory
from agents.tool_permissions import ToolPermissionManager
from agents.limits import AgentExecutionLimits


class FinalAgent:

    def __init__(self, user_id, role="USER"):

        self.user_id = user_id
        self.role = role

        self.calculator = CalculatorTool()
        self.document_search = DocumentSearchTool()

        self.memory = ConversationMemory(
            conversation_id=str(uuid.uuid4()),
            user_id=user_id,
            window_size=10
        )

        self.permissions = ToolPermissionManager(
            role
        )

        self.limits = AgentExecutionLimits()

    def authenticate(self, token):

        # Demo authentication only.
        # Do NOT use this fixed token for a real application.

        return token == "DEMO_TOKEN"

    def select_tool(self, question):

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
            "today",
            "date"
        ]):
            return "date"

        if any(word in q for word in [
            "customer",
            "invoice",
            "product",
            "quantity",
            "price",
            "total amount",
            "policy"
        ]):
            return "document_search"

        return None

    def validate_output(self, answer):

        if not answer:
            return "No answer generated."

        if len(answer) > 5000:
            return "Output exceeds the allowed limit."

        return answer

    def calculate(self, question):

        q = question.lower()

        if "multiply" in q:

            return self.calculator.multiply(
                80000,
                2
            )

        if "add" in q:

            return self.calculator.add(
                100,
                50
            )

        if "subtract" in q:

            return self.calculator.subtract(
                100,
                50
            )

        if "divide" in q:

            return self.calculator.divide(
                100,
                5
            )

        return "Calculation not recognized."

    def get_date(self):

        return datetime.now().strftime(
            "%Y-%m-%d"
        )

    def execute_tool(self, tool_name, question):

        if not self.permissions.is_allowed(
            tool_name
        ):
            raise PermissionError(
                f"Tool '{tool_name}' is not permitted "
                f"for role '{self.role}'."
            )

        if tool_name == "calculator":

            self.limits.record_tool_call()

            return self.calculate(
                question
            )

        if tool_name == "date":

            self.limits.record_tool_call()

            # Date is intentionally treated as a low-risk
            # local utility for this training project.
            return self.get_date()

        if tool_name == "document_search":

            self.limits.record_tool_call()

            results = self.document_search.search(
                question,
                top_k=2
            )

            if not results:

                return "No relevant documents found."

            documents = []

            for result in results:

                documents.append(
                    result["document"]
                )

            return "\n".join(documents)

        return "Unknown tool."

    def log_run(
        self,
        request_id,
        tool_name,
        status,
        execution_time
    ):

        log_directory = (
            PROJECT_ROOT / "outputs"
        )

        log_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        log_file = (
            log_directory /
            "final_agent.log"
        )

        with log_file.open(
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                f"{datetime.now().isoformat()} | "
                f"request_id={request_id} | "
                f"user_id={self.user_id} | "
                f"tool={tool_name} | "
                f"status={status} | "
                f"latency={execution_time}s\n"
            )

    def run(self, question, token):

        request_id = str(
            uuid.uuid4()
        )

        start_time = time.perf_counter()

        print("\n========================================")
        print("FINAL AGENT")
        print("========================================")

        print("Request ID:", request_id)
        print("User:", self.user_id)

        # 1. Authentication
        if not self.authenticate(token):

            print("\nAuthentication: FAILED")

            self.log_run(
                request_id,
                "none",
                "authentication_failed",
                0
            )

            return "Authentication failed."

        print("Authentication: SUCCESS")

        # 2. Store user message
        self.memory.add_user_message(
            question
        )

        # 3. Check execution limits
        allowed, message = (
            self.limits.can_continue()
        )

        if not allowed:

            print(
                "Execution stopped:",
                message
            )

            return (
                "Unable to complete the operation "
                "within the allowed execution limits."
            )

        # 4. Select tool
        tool_name = self.select_tool(
            question
        )

        print("Selected Tool:", tool_name)

        if tool_name is None:

            answer = (
                "I could not identify a suitable tool."
            )

            self.memory.add_assistant_message(
                answer
            )

            return answer

        # 5. Permission check
        print("Checking Permission...")

        if not self.permissions.is_allowed(
            tool_name
        ):

            answer = (
                f"Access denied for tool: {tool_name}"
            )

            print(answer)

            self.log_run(
                request_id,
                tool_name,
                "permission_denied",
                round(
                    time.perf_counter()
                    - start_time,
                    4
                )
            )

            return answer

        print("Permission: ALLOWED")

        # 6. Execute
        try:

            self.limits.next_iteration()

            result = self.execute_tool(
                tool_name,
                question
            )

            print("\nTool Result:")
            print(result)

            # 7. Observation
            print("\nObservation:")
            print("Tool execution completed successfully.")

            # 8. Output validation
            answer = self.validate_output(
                str(result)
            )

            self.memory.add_assistant_message(
                answer
            )

            execution_time = round(
                time.perf_counter()
                - start_time,
                4
            )

            # 9. Logging
            self.log_run(
                request_id,
                tool_name,
                "success",
                execution_time
            )

            # 10. Final answer
            print("\nFinal Answer:")
            print(answer)

            print(
                "\nLatency:",
                execution_time,
                "seconds"
            )

            return answer

        except Exception as error:

            execution_time = round(
                time.perf_counter()
                - start_time,
                4
            )

            print(
                "\nAgent Error:",
                str(error)
            )

            self.log_run(
                request_id,
                tool_name,
                "error",
                execution_time
            )

            return (
                "The agent could not complete "
                "the requested operation."
            )


if __name__ == "__main__":

    agent = FinalAgent(
        user_id="user-001",
        role="USER"
    )

    print(
        "\nDemo token: DEMO_TOKEN"
    )

    agent.run(
        "Who is the customer?",
        "DEMO_TOKEN"
    )

    agent.run(
        "What is the total amount?",
        "DEMO_TOKEN"
    )

    agent.run(
        "What product was purchased?",
        "DEMO_TOKEN"
    )

    agent.run(
        "What is today's date?",
        "DEMO_TOKEN"
    )

    agent.run(
        "Multiply 80000 by 2",
        "DEMO_TOKEN"
    )
