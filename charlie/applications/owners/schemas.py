from datetime import date
from pydantic import BaseModel, EmailStr, Field


# WORKING IN PROGRESS
class OwnerIn(BaseModel):
    name: str
    email: EmailStr
    picture: str  # necessary? s3 url
    birthday: date


class OwnerOut(OwnerIn):
    id: str = Field(..., alias="_id")


class Owner_Update(BaseModel):
    name: str | None = None
    picture: str | None = None
