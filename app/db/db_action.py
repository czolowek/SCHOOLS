from jose import jwt
from app.db.models import User
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def get_user_by_token(token: str) -> User:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    username = payload.get("sub")
    if not username:
        raise ValueError("Invalid token")
    return User(username=username)
