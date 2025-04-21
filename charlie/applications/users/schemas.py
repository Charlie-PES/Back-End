from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    username: str
    cpf: str
    email: str
    tutor: bool
    adopter: bool


class UserIn(BaseModel):
    username: str
    cpf: str
    email: str
    password: str
    tutor: bool
    adopter: bool


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
