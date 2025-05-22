from fastapi import APIRouter, status

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from .base import AIAgent
from .schemas import UserMessage, AIMessage


chat_router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
    route_class=DishkaRoute
)


@chat_router.post(
    path="/completion",
    status_code=status.HTTP_200_OK,
    response_model=AIMessage
)
async def answer(
        user_message: UserMessage,
        ai_agent: FromDishka[AIAgent]
) -> AIMessage:
    generated = await ai_agent.generate(user_message.chat_id, user_message.text)
    return AIMessage(chat_id=user_message.chat_id, text=generated)
