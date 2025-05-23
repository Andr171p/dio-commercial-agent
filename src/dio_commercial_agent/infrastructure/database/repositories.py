from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.dio_commercial_agent.core.base import MessageRepository
from src.dio_commercial_agent.core.entities import BaseMessage
from .models import MessageOrm


class SQLMessageRepository(MessageRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    async def bulk_create(self, messages: list[BaseMessage]) -> None:
        try:
            message_orms = [MessageOrm(**message.model_dump()) for message in messages]
            async with self.session_factory() as session:
                session.add_all(message_orms)
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise RuntimeError(f"Error while bulk creating messages: {e}")

    async def read(self, chat_id: str) -> Optional[list[BaseMessage]]:
        try:
            async with self.session_factory() as session:
                stmt = (
                    select(MessageOrm)
                    .where(MessageOrm.chat_id == chat_id)
                )
                results = await session.execute(stmt)
            messages = results.scalars().all()
            return [BaseMessage.model_validate(message) for message in messages] if messages else None
        except SQLAlchemyError as e:
            await session.rollback()
            raise RuntimeError(f"Error while reading messages: {e}")
