import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Conversation, Message


class NotFoundError(Exception):
    pass


def title_from_message(message: str) -> str:
    words = " ".join(message.split())
    return words[:57].rstrip() + "..." if len(words) > 60 else words or "New conversation"


class ConversationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, title: str = "New conversation") -> Conversation:
        item = Conversation(title=title)
        self.session.add(item)
        await self.session.commit()
        return await self.get(item.id)

    async def list(self) -> list[Conversation]:
        result = await self.session.scalars(select(Conversation).order_by(Conversation.updated_at.desc()))
        return list(result)

    async def get(self, conversation_id: uuid.UUID) -> Conversation:
        stmt = (
            select(Conversation).where(Conversation.id == conversation_id).options(selectinload(Conversation.messages))
        )
        item = await self.session.scalar(stmt)
        if item is None:
            raise NotFoundError("Conversation not found.")
        return item

    async def update_title(self, conversation_id: uuid.UUID, title: str) -> Conversation:
        item = await self.get(conversation_id)
        item.title = title
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete(self, conversation_id: uuid.UUID) -> None:
        item = await self.get(conversation_id)
        await self.session.delete(item)
        await self.session.commit()

    async def add_message(
        self,
        conversation_id: uuid.UUID,
        role: str,
        content: str,
        status: str = "completed",
        provider: str | None = None,
        model: str | None = None,
    ) -> Message:
        conversation = await self.get(conversation_id)
        if conversation.title == "New conversation" and role == "user":
            conversation.title = title_from_message(content)
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            status=status,
            provider=provider,
            model=model,
        )
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message
