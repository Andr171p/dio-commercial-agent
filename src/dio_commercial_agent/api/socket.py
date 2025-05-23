from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject

from ..core.base import AIAgent
from ..core.entities import UserMessage
from ..infrastructure.websockets import BaseSocketManager


chat_socket = APIRouter(
    prefix="/api/v1/ws/chat",
    tags=["Streaming chat"],
    route_class=DishkaRoute
)


@chat_socket.websocket("/{chat_id}")
@inject
async def streaming_generate(
        websocket: WebSocket,
        chat_id: str,
        ai_agent: FromDishka[AIAgent],
        socket_manager: FromDishka[BaseSocketManager],
) -> None:
    await socket_manager.connect(websocket, chat_id)
    try:
        while True:
            message = await websocket.receive_json()
            user_message = UserMessage.model_validate(message)
            ai_message = await ai_agent.generate(user_message)
            await socket_manager.send(chat_id, ai_message)
    except WebSocketDisconnect:
        await socket_manager.disconnect(chat_id)
