from typing import Optional

from abc import ABC, abstractmethod

from .schemas import BaseMessage


class AIAgent(ABC):
    @abstractmethod
    async def generate(self, chat_id: str, text: str) -> str: pass


class MessageRepository(ABC):
    @abstractmethod
    async def bulk_create(self, messages: list[BaseMessage]) -> None: pass

    @abstractmethod
    async def read(self, chat_id: str) -> Optional[list[BaseMessage]]: pass
