from typing import TypedDict
from uuid import UUID


class GraphState(TypedDict, total=False):
    conversation_id: UUID
    user_message: str
    assistant_message: str
    provider: str
    model: str
