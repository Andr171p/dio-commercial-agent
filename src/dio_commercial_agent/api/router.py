from fastapi import APIRouter, status, HTTPException

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from ..core.base import AIAgent
from ..core.entities import UserMessage, AIMessage


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
async def generate(user_message: UserMessage, ai_agent: FromDishka[AIAgent]) -> AIMessage:
    ai_message = await ai_agent.generate(user_message)
    if not ai_message:
        raise HTTPException(status_code=500, detail="Error while generating response")
    return ai_message
