import asyncio

from src.memory.state import AgentState
from src.memory.memory_agent import MemoryAgent

from src.agents.supervisor import SupervisorAgent
from src.agents.researcher import ResearchAgent
from src.agents.rag_agent import RAGAgent
from src.agents.analyst import AnalystAgent
from src.agents.validator import ValidatorAgent
from src.agents.writer import WriterAgent

from src.tools.selector import ToolSelector
from src.tools.executor import ToolExecutor

from src.orchestration.agent_runner import AgentRunner
from src.orchestration.execution_tracker import ExecutionTracker
from src.orchestration.parallel_executor import ParallelExecutor


class MultiAgentWorkflow:
    """
    Complete Multi-Agent AI workflow.

    Memory
        ↓
    Supervisor
        ↓
    Tools
        ↓
    Parallel:
        ├── Researcher
        └── RAG
        ↓
    Analyst
        ↓
    Validator
        ↓
    Writer
    """

    def __init__(self):

        # Memory
        self.memory = MemoryAgent()

        # Agents
        self.supervisor = SupervisorAgent()
        self.researcher = ResearchAgent()
        self.rag = RAGAgent()
        self.analyst = AnalystAgent()
        self.validator = ValidatorAgent()
        self.writer = WriterAgent()

        # Tools
        self.tool_selector = ToolSelector()
        self.tool_executor = ToolExecutor()

        # Tracking
        self.execution_tracker = ExecutionTracker()

        # Agent runner
        self.agent_runner = AgentRunner(
            max_attempts=3,
            execution_tracker=self.execution_tracker
        )

        # Parallel executor
        self.parallel_executor = ParallelExecutor()

    # =====================================================
    # PARALLEL RESEARCH
    # =====================================================

    async def _parallel_research(
        self,
        state: AgentState
    ):

        async def research_task():

            return await asyncio.to_thread(
                self.researcher.research,
                state
            )

        async def rag_task():

            return await asyncio.to_thread(
                self.rag.retrieve,
                state
            )

        results = await self.parallel_executor.run(
            research_task,
            rag_task
        )

        return results

    # =====================================================
    # MAIN WORKFLOW
    # =====================================================

    def run(
        self,
        state: AgentState
    ) -> AgentState:

        print()
        print("=" * 60)
        print("STARTING MULTI-AGENT WORKFLOW")
        print("=" * 60)

        state.task_status = "started"

        # =================================================
        # 1. MEMORY
        # =================================================

        state.current_agent = "Memory"

        previous_state = (
            self.memory.retrieve_previous_state(
                state
            )
        )

        if previous_state:

            print(
                "[Memory] Previous conversation found."
            )

            if previous_state.tool_results:

                state.tool_results.extend(
                    previous_state.tool_results
                )

            if previous_state.research_results:

                state.research_results.extend(
                    previous_state.research_results
                )

            if previous_state.retrieved_documents:

                state.retrieved_documents.extend(
                    previous_state.retrieved_documents
                )

        else:

            print(
                "[Memory] No previous conversation found."
            )

        # =================================================
        # 2. SUPERVISOR
        # =================================================

        state.current_agent = "Supervisor"

        next_agent = (
            self.supervisor.decide_next_agent(
                state
            )
        )

        print(
            f"[Supervisor] Next agent: {next_agent}"
        )

        # =================================================
        # 3. TOOL CALLING
        # =================================================

        if self.supervisor.requires_tool(
            state.user_request
        ):

            state.current_agent = "ToolSelector"

            selected_tool = (
                self.tool_selector.select(
                    state.user_request
                )
            )

            print(
                f"[ToolSelector] "
                f"Selected tool: {selected_tool}"
            )

            state.current_agent = "ToolExecutor"

            if selected_tool == "calculator":

                tool_result = (
                    self.tool_executor.execute(
                        selected_tool,
                        expression=state.user_request
                    )
                )

            elif selected_tool == "document_reader":

                tool_result = (
                    self.tool_executor.execute(
                        selected_tool,
                        document_name=state.user_request
                    )
                )

            elif selected_tool == "validation_tool":

                tool_result = (
                    self.tool_executor.execute(
                        selected_tool,
                        data=state.user_request
                    )
                )

            else:

                tool_result = (
                    self.tool_executor.execute(
                        selected_tool,
                        query=state.user_request
                    )
                )

            if isinstance(
                tool_result,
                dict
            ):

                state.tool_results.append(
                    tool_result
                )

                if not tool_result.get(
                    "success",
                    True
                ):

                    state.errors.append({
                        "agent": "ToolExecutor",
                        "tool": selected_tool,
                        "message": tool_result.get(
                            "error",
                            "Tool execution failed."
                        )
                    })

            else:

                state.tool_results.append({
                    "tool": selected_tool,
                    "result": tool_result
                })

        else:

            print(
                "[Supervisor] No tool required."
            )

        # =================================================
        # 4. PARALLEL RESEARCH + RAG
        # =================================================

        print()
        print("=" * 60)
        print("STARTING PARALLEL RESEARCH + RAG")
        print("=" * 60)

        state.task_status = "parallel_execution"

        try:

            asyncio.run(
                self._parallel_research(
                    state
                )
            )

        except Exception as exc:

            state.errors.append({
                "agent": "ParallelExecutor",
                "message": str(exc)
            })

            state.task_status = "parallel_failed"

            print(
                f"[ParallelExecutor] Failed: {exc}"
            )

            return state

        # =================================================
        # 5. ANALYST
        # =================================================

        print()
        print(
            "[Workflow] Starting Analyst..."
        )

        state = self.agent_runner.run(
            state,
            "Analyst",
            self.analyst.analyze
        )

        if state.task_status == "agent_failed":

            return state

        # =================================================
        # 6. VALIDATOR
        # =================================================

        print()
        print(
            "[Workflow] Starting Validator..."
        )

        state = self.agent_runner.run(
            state,
            "Validator",
            self.validator.validate
        )

        if state.task_status == "agent_failed":

            return state

        if state.task_status == "validation_failed":

            return state

        # =================================================
        # 7. WRITER
        # =================================================

        print()
        print(
            "[Workflow] Starting Writer..."
        )

        state = self.agent_runner.run(
            state,
            "Writer",
            self.writer.write
        )

        if state.task_status == "agent_failed":

            return state

        # =================================================
        # 8. COMPLETE
        # =================================================

        state.task_status = "completed"

        print()
        print("=" * 60)
        print(
            "MULTI-AGENT WORKFLOW COMPLETED"
        )
        print("=" * 60)

        return state


def create_workflow():

    return MultiAgentWorkflow()