from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject

from .base import AIAgent
from .schemas import UserMessage, AIMessage
from .infrastructure.connection_managers import BaseConnectionManager


socket_chat_router = APIRouter(
    prefix="/api/v1/ws/chat",
    tags=["Streaming chat"],
    route_class=DishkaRoute
)


@socket_chat_router.websocket("/{chat_id}")
@inject
async def streaming_generate(
        websocket: WebSocket,
        chat_id: str,
        ai_agent: FromDishka[AIAgent],
        connection_manager: FromDishka[BaseConnectionManager],
) -> None:
    await connection_manager.connect(websocket, chat_id)
    try:
        while True:
            message = await websocket.receive_json()
            user_message = UserMessage.model_validate(message)
            generated = await ai_agent.generate(user_message.chat_id, user_message.text)
            ai_message = AIMessage(chat_id=user_message.chat_id, text=generated)
            await connection_manager.send(chat_id, ai_message)
    except WebSocketDisconnect:
        await connection_manager.disconnect(chat_id)
