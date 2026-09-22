import json
import uuid
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.db.repositories import ConversationRepository
from app.graph.builder import build_graph
from app.graph.nodes import build_messages, create_chat_model, normalize_text
from app.schemas.chat import ChatRequest


class ChatService:
    def __init__(self, session: AsyncSession, settings: Settings):
        self.repository = ConversationRepository(session)
        self.settings = settings
        self.model = create_chat_model(settings)

    async def send(self, payload: ChatRequest):
        await self.repository.add_message(payload.conversation_id, "user", payload.message)
        graph = build_graph(self.model, self.settings)
        state = await graph.ainvoke(
            {"conversation_id": payload.conversation_id, "user_message": payload.message},
            config={"configurable": {"thread_id": str(payload.conversation_id)}},
        )
        return await self.repository.add_message(
            payload.conversation_id,
            "assistant",
            state["assistant_message"],
            provider=state.get("provider"),
            model=state.get("model"),
        )

    async def stream(self, payload: ChatRequest) -> AsyncIterator[str]:
        await self.repository.add_message(payload.conversation_id, "user", payload.message)
        message_id = uuid.uuid4()
        yield _sse("metadata", {"conversation_id": str(payload.conversation_id), "message_id": str(message_id)})
        chunks: list[str] = []
        try:
            async for chunk in self.model.astream(build_messages(payload.message)):
                text = normalize_text(chunk)
                if text:
                    chunks.append(text)
                    yield _sse("delta", {"content": text})
            content = "".join(chunks).strip()
            await self.repository.add_message(
                payload.conversation_id,
                "assistant",
                content,
                provider="fake" if self.settings.fake_llm else self.settings.llm_provider,
                model=self.settings.llm_model,
            )
            yield _sse("done", {"finish_reason": "stop"})
        except Exception:
            await self.repository.add_message(
                payload.conversation_id,
                "assistant",
                "The assistant response failed.",
                status="failed",
                provider="fake" if self.settings.fake_llm else self.settings.llm_provider,
                model=self.settings.llm_model,
            )
            yield _sse("error", {"code": "PROVIDER_ERROR", "message": "The assistant is unavailable."})


def _sse(event: str, data: dict[str, str]) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"
