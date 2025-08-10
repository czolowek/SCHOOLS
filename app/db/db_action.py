import os
from dotenv import load_dotenv
from jose import jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.models import User

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def get_user_by_token(token: str) -> User:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return User(username=username)