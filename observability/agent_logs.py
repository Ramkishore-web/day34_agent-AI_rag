import json
import time
import uuid
from pathlib import Path


LOG_FILE = Path("outputs/agent_logs.jsonl")


class AgentLogger:

    def __init__(self):

        LOG_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def log_run(
        self,
        user_id,
        agent_id,
        tool_selected,
        tool_arguments,
        tool_result_status,
        iteration,
        final_result,
        execution_time
    ):

        request_id = str(uuid.uuid4())

        log_data = {
            "request_id": request_id,
            "user_id": user_id,
            "agent_id": agent_id,
            "tool_selected": tool_selected,
            "tool_arguments": tool_arguments,
            "tool_result_status": tool_result_status,
            "execution_time_seconds": execution_time,
            "iteration": iteration,
            "final_result": final_result
        }

        with LOG_FILE.open(
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(log_data)
                + "\n"
            )

        return request_id


if __name__ == "__main__":

    logger = AgentLogger()

    start_time = time.perf_counter()

    # Example agent execution
    time.sleep(0.1)

    execution_time = round(
        time.perf_counter() - start_time,
        4
    )

    request_id = logger.log_run(
        user_id="user-001",
        agent_id="company_assistant",
        tool_selected="document_search",
        tool_arguments={
            "query": "What is the leave policy?"
        },
        tool_result_status="success",
        iteration=1,
        final_result="Leave policy information retrieved.",
        execution_time=execution_time
    )

    print("Agent log created.")
    print("Request ID:", request_id)
    print("Execution Time:", execution_time, "seconds")
    print("Log File:", LOG_FILE)
