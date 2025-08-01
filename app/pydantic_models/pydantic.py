from pydantic import BaseModel, Field
from typing import Optional

class Message(BaseModel):
    content: str = Field(..., max_length=1000)

class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[str] = None
