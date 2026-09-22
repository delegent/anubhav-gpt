import uuid

import pytest
from pydantic import ValidationError

from app.schemas.chat import ChatRequest


def test_chat_request_accepts_valid_payload():
    payload = ChatRequest(conversation_id=uuid.uuid4(), message="  Explain LangGraph.  ")
    assert payload.message == "Explain LangGraph."


@pytest.mark.parametrize(
    "message",
    ["", "   ", "x" * 8001],
)
def test_chat_request_rejects_invalid_message(message):
    with pytest.raises(ValidationError):
        ChatRequest(conversation_id=uuid.uuid4(), message=message)


def test_chat_request_rejects_extra_fields():
    with pytest.raises(ValidationError):
        ChatRequest(conversation_id=uuid.uuid4(), message="hello", raw_provider="nope")
