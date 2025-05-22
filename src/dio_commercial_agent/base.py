from abc import ABC, abstractmethod


class AIAgent(ABC):
    @abstractmethod
    async def generate(self, chat_id: str, text: str) -> str: pass


class MessagesRepository(ABC):
    pass
