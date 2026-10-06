from typing import Optional

from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Question for the multi-agent AI system"
    )

    conversation_id: Optional[str] = Field(
        default=None,
        description="Conversation ID used to maintain memory"
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty")

        return value


class QueryResponse(BaseModel):
    status: str
    question: str
    answer: str
    processing_time_seconds: float