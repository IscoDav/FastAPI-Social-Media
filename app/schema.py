from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBased(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBased):
    pass


class Post(PostBased):
    id: int
    created_at: datetime
    owner_id : int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    password: str


class TokenData(BaseModel):
    id: Optional[str] = None
