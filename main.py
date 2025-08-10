import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from app.db.models import Base
from app.routes.route import router as chat_router
from app.routes.school import router as school_router

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(school_router, prefix="/api")
app.include_router(chat_router, prefix="")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)