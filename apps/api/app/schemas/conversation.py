from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ConversationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(default="New conversation", min_length=1, max_length=120)

    @field_validator("title")
    @classmethod
    def trim_title(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Title must not be blank.")
        return trimmed


class ConversationUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=120)

    @field_validator("title")
    @classmethod
    def trim_title(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Title must not be blank.")
        return trimmed


class MessageResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: UUID
    role: str
    content: str
    status: str
    created_at: datetime


class ConversationSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime


class ConversationDetail(ConversationSummary):
    messages: list[MessageResponse] = Field(default_factory=list)
