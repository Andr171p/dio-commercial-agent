from typing import Literal

from pydantic import BaseModel


class BaseMessage(BaseModel):
    role: Literal["user", "ai"]
    chat_id: str
    text: str


class UserMessage(BaseMessage):
    role: str = "user"


class AIMessage(BaseMessage):
    role: str = "ai"
