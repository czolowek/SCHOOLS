from typing import List, Optional
import enum
import asyncio

from sqlalchemy import String, Integer, ForeignKey, Column, Enum
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings

engine = create_async_engine(settings, echo=True)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

class Role(enum.Enum):
    student = enum.auto()
    teacher = enum.auto()
    admin = enum.auto()
    editor = enum.auto()









