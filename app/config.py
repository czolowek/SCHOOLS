from fastapi import WebSocket
from typing import Dict
from html import escape
from app.pydantic_models.pydantic import Message

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, class_id: int, username: str, websocket: WebSocket):
        await websocket.accept()
        key = f"{class_id}:{username}"
        self.active_connections[key] = websocket

    def disconnect(self, class_id: int, username: str):
        key = f"{class_id}:{username}"
        if key in self.active_connections:
            del self.active_connections[key]

    async def broadcast(self, class_id: int, message: Message, sender: str):
        sanitized = escape(message.content)
        prefix = f"{class_id}:"
        for key, conn in list(self.active_connections.items()):
            cid, user = key.split(":", 1)
            if int(cid) == class_id and user != sender:
                await conn.send_json({"from": sender, "message": sanitized})

manager = ConnectionManager()