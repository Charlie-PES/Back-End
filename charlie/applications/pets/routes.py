from collections.abc import Iterable
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from utils.pyobjectid import PyObjectId
from dependencies.database import get_database
from .schemas import PetIn
from .models import PetDAO
from settings import Settings
from motor.motor_asyncio import AsyncIOMotorClient
from . import controllers as pets_controllers

settings = Settings()
router = APIRouter(tags=["pets"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_one(
    body: PetIn, db: AsyncIOMotorClient = Depends(get_database)
) -> PetDAO:
    return await pets_controllers.create_one(pet_in=body, db=db)


@router.get("/{pet_id}", status_code=status.HTTP_200_OK)
async def read_one(
    pet_id: PyObjectId, db: AsyncIOMotorClient = Depends(get_database)
) -> PetDAO:
    return await pets_controllers.read_one(pet_id=pet_id, db=db)


@router.get("", status_code=status.HTTP_200_OK)
async def read_many(
    is_available: bool | None = Query(None),
    db: AsyncIOMotorClient = Depends(get_database),
) -> Iterable[PetDAO]:
    return await pets_controllers.read_many(db=db, is_available=is_available)


@router.delete("/{pet_id}", status_code=status.HTTP_200_OK)
async def delete_one(
    pet_id: PyObjectId,
    db: AsyncIOMotorClient = Depends(get_database),
) -> None:
    return await pets_controllers.delete_one(db=db, pet_id=pet_id)
