from fastapi import FastAPI
from pydantic import BaseModel

from src.memory.state import AgentState
from src.orchestration.workflow import MultiAgentWorkflow


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="Multi-Agent AI API",
    version="1.0"
)


# =========================================================
# Workflow
# =========================================================

workflow = MultiAgentWorkflow()


# =========================================================
# Request Model
# =========================================================

class QueryRequest(BaseModel):
    question: str
    conversation_id: str = "default"


# =========================================================
# Root Endpoint
# =========================================================

@app.get("/")
def root():

    return {
        "status": "success",
        "message": "Multi-Agent AI API is running"
    }


# =========================================================
# Health Endpoint
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "multi-agent-ai"
    }


# =========================================================
# Query Endpoint
# =========================================================

@app.post("/query")
def query(request: QueryRequest):

    # -----------------------------------------------------
    # Create AgentState
    # -----------------------------------------------------

    state = AgentState(
        conversation_id=request.conversation_id,
        user_request=request.question
    )

    # -----------------------------------------------------
    # Run Multi-Agent Workflow
    # -----------------------------------------------------

    result = workflow.run(state)

    # -----------------------------------------------------
    # Get Execution History
    # -----------------------------------------------------

    execution_events = (
        workflow.execution_tracker.get_events()
    )

    # -----------------------------------------------------
    # Return Final Response
    # -----------------------------------------------------

    return {
        "status": result.task_status,
        "question": result.user_request,
        "answer": result.final_response,
        "current_agent": result.current_agent,
        "errors": result.errors,
        "execution_history": execution_events
    }