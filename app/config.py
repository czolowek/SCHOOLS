from fastapi import WebSocket
from typing import Dict
from html import escape
from app.pydantic_models.pydantic import Message

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, username: str):
        if username in self.active_connections:
            del self.active_connections[username]

    async def broadcast(self, message: Message, sender: str):
        sanitized = escape(message.content)
        for user, conn in self.active_connections.items():
            await conn.send_json({
                "from": sender,
                "message": sanitized
            })

manager = ConnectionManager()
