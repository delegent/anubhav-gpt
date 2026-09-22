from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import ConversationRepository
from app.schemas.conversation import ConversationCreate, ConversationUpdate


class ConversationService:
    def __init__(self, session: AsyncSession):
        self.repository = ConversationRepository(session)

    async def create(self, payload: ConversationCreate):
        return await self.repository.create(payload.title)

    async def list(self):
        return await self.repository.list()

    async def get(self, conversation_id: UUID):
        return await self.repository.get(conversation_id)

    async def update(self, conversation_id: UUID, payload: ConversationUpdate):
        return await self.repository.update_title(conversation_id, payload.title)

    async def delete(self, conversation_id: UUID) -> None:
        await self.repository.delete(conversation_id)
