from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    username: str
    email: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
