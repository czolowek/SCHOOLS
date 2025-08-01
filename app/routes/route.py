from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.db.db_action import get_user_by_token
from app.routes.config import manager
from app.pydantic_models.pydantic import Message
from jose import JWTError

router = APIRouter()

@router.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        user = get_user_by_token(token)
        await manager.connect(user.username, websocket)
    except JWTError:
        await websocket.close(code=1008)
        return
    except Exception:
        await websocket.close(code=1011)
        return
    try:
        while True:
            data = await websocket.receive_json()
            msg = Message(**data)
            await manager.broadcast(msg, user.username)
    except WebSocketDisconnect:
        manager.disconnect(user.username)
