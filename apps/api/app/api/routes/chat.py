from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import db_session, settings
from app.core.config import Settings
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest, session: AsyncSession = Depends(db_session), app_settings: Settings = Depends(settings)
):
    message = await ChatService(session, app_settings).send(payload)
    return ChatResponse(
        conversation_id=message.conversation_id,
        message_id=message.id,
        role=message.role,
        content=message.content,
        created_at=message.created_at,
    )


@router.post("/stream")
async def chat_stream(
    payload: ChatRequest,
    session: AsyncSession = Depends(db_session),
    app_settings: Settings = Depends(settings),
):
    service = ChatService(session, app_settings)
    return StreamingResponse(service.stream(payload), media_type="text/event-stream")
