from typing import Optional, Union

from uuid import UUID
from abc import ABC, abstractmethod

from pydantic import BaseModel

from fastapi import WebSocket


class BaseConnectionManager(ABC):
    @abstractmethod
    async def connect(self, websocket: WebSocket, connection_id: Union[str, UUID]) -> None: pass

    @abstractmethod
    async def disconnect(self, connection_id: Union[str, UUID]) -> None: pass

    @abstractmethod
    async def get_connection(self, connection_id: Union[str, UUID]) -> Optional[WebSocket]: pass

    async def send(self, connection_id: Union[str, UUID], data: BaseModel) -> None:
        connection = await self.get_connection(connection_id)
        if connection is None:
            return
        await connection.send_json(data.model_dump())
