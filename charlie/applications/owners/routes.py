from fastapi import APIRouter, Depends, status

from charlie.applications.owners.models import OwnerDAO
from charlie.applications.owners.schemas import (
    LoginRequest,
    LoginResponse,
    OwnerOut,
    OwnerIn,
)
from charlie.utils.pyobjectid import PyObjectId
from charlie.applications.owners import controllers as owner_controllers
from charlie.dependencies.database import get_database
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter(prefix="/owners", tags=["owners"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(owner: OwnerIn, db: AsyncIOMotorClient = Depends(get_database)):
    return await owner_controllers.register_owner(owner_in=owner, db=db)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    login_data: LoginRequest, db: AsyncIOMotorClient = Depends(get_database)
) -> LoginResponse:
    return await owner_controllers.login(login_data=login_data, db=db)


@router.get("/{owner_id}", status_code=status.HTTP_200_OK)
async def read_one(
    owner_id: PyObjectId, db: AsyncIOMotorClient = Depends(get_database)
) -> OwnerOut:
    return await owner_controllers.read_one(owner_id=owner_id, db=db)


@router.get("", status_code=status.HTTP_200_OK)
async def read_many(
    db: AsyncIOMotorClient = Depends(get_database),
) -> list[OwnerDAO]:
    return await owner_controllers.read_many(db=db)
