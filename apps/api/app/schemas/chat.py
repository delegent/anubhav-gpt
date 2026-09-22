from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    conversation_id: UUID
    message: str = Field(min_length=1, max_length=8000)

    @field_validator("message")
    @classmethod
    def trim_message(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Message must not be blank.")
        return trimmed


class ChatResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    conversation_id: UUID
    message_id: UUID
    role: str
    content: str
    created_at: datetime
