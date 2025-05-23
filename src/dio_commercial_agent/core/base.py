from typing import Optional

from abc import ABC, abstractmethod

from .entities import BaseMessage, UserMessage, AIMessage


class AIAgent(ABC):
    @abstractmethod
    async def generate(self, user_message: UserMessage) -> AIMessage: pass


class MessageRepository(ABC):
    @abstractmethod
    async def bulk_create(self, messages: list[BaseMessage]) -> None: pass

    @abstractmethod
    async def read(self, chat_id: str) -> Optional[list[BaseMessage]]: pass
