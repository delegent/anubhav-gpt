import asyncio
from collections.abc import AsyncIterator
from typing import Any, Protocol, cast

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.core.config import Settings
from app.graph.prompts import SYSTEM_PROMPT
from app.graph.state import GraphState


class ChatModel(Protocol):
    async def ainvoke(self, messages: list[object]) -> Any: ...

    def astream(self, messages: list[object]) -> AsyncIterator[Any]: ...


class ProviderError(Exception):
    code = "PROVIDER_ERROR"
    status_code = 503


class FakeChatModel:
    provider = "fake"
    model = "fake-anubhavgpt"

    async def ainvoke(self, messages: list[object]) -> AIMessage:
        user_text = _last_human_text(messages)
        return AIMessage(content=_fake_answer(user_text))

    async def astream(self, messages: list[object]) -> AsyncIterator[AIMessage]:
        user_text = _last_human_text(messages)
        for token in _fake_answer(user_text).split(" "):
            await asyncio.sleep(0)
            yield AIMessage(content=f"{token} ")


def create_chat_model(settings: Settings) -> ChatModel:
    if settings.fake_llm or settings.llm_provider == "fake":
        return FakeChatModel()
    if settings.llm_provider != "google_genai":
        raise ProviderError("Unsupported LLM provider.")
    if not settings.google_api_key:
        raise ProviderError("GOOGLE_API_KEY is required when FAKE_LLM=false.")
    model = init_chat_model(
        f"google_genai:{settings.llm_model}",
        timeout=settings.llm_timeout_seconds,
        max_retries=2,
    )
    return cast(ChatModel, model)


def build_messages(user_message: str) -> list[object]:
    return [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=user_message)]


def normalize_text(message: object) -> str:
    raw = getattr(message, "content", message)
    if isinstance(raw, str):
        return raw.strip()
    if isinstance(raw, list):
        parts: list[str] = []
        for item in raw:
            if isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts).strip()
    content = getattr(message, "text", None)
    if isinstance(content, str):
        return content.strip()
    if callable(content):
        return str(content()).strip()
    return str(raw).strip()


async def validate_context_node(state: GraphState) -> GraphState:
    if not state.get("conversation_id") or not state.get("user_message"):
        raise ValueError("Graph state is missing required conversation context.")
    return state


async def assistant_model_node(state: GraphState, model: ChatModel, settings: Settings) -> GraphState:
    try:
        response = await model.ainvoke(build_messages(state["user_message"]))
    except Exception as exc:  # Provider libraries raise heterogeneous exceptions.
        raise ProviderError("The model provider is unavailable.") from exc
    state["assistant_message"] = normalize_text(response)
    state["provider"] = "fake" if settings.fake_llm else settings.llm_provider
    state["model"] = settings.llm_model
    return state


async def persist_result_node(state: GraphState) -> GraphState:
    return state


def _last_human_text(messages: list[object]) -> str:
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            return normalize_text(message)
    return ""


def _fake_answer(user_text: str) -> str:
    topic = user_text.rstrip(".?!") or "this request"
    return (
        f"### AnubhavGPT response\n\n"
        f"- I understood the request: `{topic}`.\n"
        "- In fake-model mode this response is deterministic for tests and local development.\n"
        "- Replace `FAKE_LLM=true` with Gemini settings when you want live model calls.\n\n"
        "A practical next step is to inspect the relevant code path, reproduce the issue, "
        "and document the resolution."
    )
