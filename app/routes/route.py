from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from app.db.db_action import get_user_by_token
from app.config import manager
from app.pydantic_models.pydantic import Message
from jose import JWTError
import html

router = APIRouter()

@router.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        user = get_user_by_token(token)
        await manager.connect(user.username, websocket)
    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    except Exception:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        return
    try:
        while True:
            data = await websocket.receive_json()
            msg = Message(**data)
            msg.content = html.escape(msg.content)
            await manager.broadcast(msg, user.username)
    except WebSocketDisconnect:
        manager.disconnect(user.username)