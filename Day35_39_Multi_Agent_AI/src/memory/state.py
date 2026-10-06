from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class AgentState:
    """Shared state for the multi-agent system."""

    conversation_id: str
    user_request: str

    current_agent: Optional[str] = None
    task_status: str = "pending"

    research_results: List[Dict[str, Any]] = field(default_factory=list)
    retrieved_documents: List[Dict[str, Any]] = field(default_factory=list)
    analysis_results: List[Dict[str, Any]] = field(default_factory=list)
    validation_results: List[Dict[str, Any]] = field(default_factory=list)
    tool_results: List[Dict[str, Any]] = field(default_factory=list)

    final_response: Optional[str] = None
    errors: List[Dict[str, Any]] = field(default_factory=list)