from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from charlie.applications.users.schemas import (
    LoginRequest,
    LoginResponse,
    UserIn,
    UserOut,
)
from charlie.utils.pyobjectid import PyObjectId
from . import controllers as user_controllers
from dependencies.database import get_database
from motor.motor_asyncio import AsyncIOMotorClient


router = APIRouter(tags=["users"])


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserIn, db: AsyncIOMotorClient = Depends(get_database)):
    return await user_controllers.register_user(user_in=user, db=db)


@router.post("/auth/login", status_code=status.HTTP_200_OK)
async def login(
    login_data: LoginRequest, db: AsyncIOMotorClient = Depends(get_database)
) -> LoginResponse:
    return await user_controllers.login(login_data=login_data, db=db)


@router.get("/auth/profile", status_code=status.HTTP_200_OK)
async def read_one(
    user_id: PyObjectId, db: AsyncIOMotorClient = Depends(get_database)
) -> UserOut:
    return await user_controllers.read_one(user_id=user_id, db=db)
