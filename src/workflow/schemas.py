
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AgentHandoff(BaseModel):
    """Validated contract between workflow agents."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=1)
    task: str = Field(min_length=1)
    from_agent: Literal["planner", "researcher", "validator"]
    to_agent: Literal["planner", "researcher", "validator"]
    status: Literal["success", "failed"]
    evidence_urls: list[str] = Field(default_factory=list)


class ResearchResult(BaseModel):
    """Research result with traceable source URLs."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=1)
    answer: str = Field(min_length=1)
    evidence_urls: list[str] = Field(min_length=1)
