import uvicorn
from fastapi import FastAPI
from app.routes.route import router
from fastapi.middleware.cors import CORSMiddleware
from app.db.models import Base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)









