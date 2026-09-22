from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import db_session
from app.schemas.conversation import (
    ConversationCreate,
    ConversationDetail,
    ConversationSummary,
    ConversationUpdate,
)
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("", response_model=ConversationDetail, status_code=status.HTTP_201_CREATED)
async def create(payload: ConversationCreate, session: AsyncSession = Depends(db_session)):
    return await ConversationService(session).create(payload)


@router.get("", response_model=list[ConversationSummary])
async def list_conversations(session: AsyncSession = Depends(db_session)):
    return await ConversationService(session).list()


@router.get("/{conversation_id}", response_model=ConversationDetail)
async def get(conversation_id: UUID, session: AsyncSession = Depends(db_session)):
    return await ConversationService(session).get(conversation_id)


@router.patch("/{conversation_id}", response_model=ConversationSummary)
async def update(conversation_id: UUID, payload: ConversationUpdate, session: AsyncSession = Depends(db_session)):
    return await ConversationService(session).update(conversation_id, payload)


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(conversation_id: UUID, session: AsyncSession = Depends(db_session)):
    await ConversationService(session).delete(conversation_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
