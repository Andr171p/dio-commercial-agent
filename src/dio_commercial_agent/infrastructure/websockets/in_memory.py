from typing import Optional, Union

import logging
from uuid import UUID

from fastapi import WebSocket

from .base import BaseSocketManager


class InMemorySocketManager(BaseSocketManager):
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, connection_id: Union[str, UUID]) -> None:
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        self.logger.info("Created new connection with id %s", connection_id)

    async def disconnect(self, connection_id: Union[str, UUID]) -> None:
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
            self.logger.info("Deleted connection by id %s", connection_id)

    async def get_connection(self, connection_id: Union[str, UUID]) -> Optional[WebSocket]:
        return self.active_connections.get(connection_id)
