from collections.abc import Iterable
from fastapi import APIRouter, Depends, status
from utils.pyobjectid import PyObjectId
from dependencies.database import get_database
from .models import AdoptionDAO
from settings import Settings
from motor.motor_asyncio import AsyncIOMotorClient
from . import controllers as adoption_controllers

settings = Settings()
router = APIRouter(tags=["adoption"])


@router.post(
    "/request/pet_id/{pet_id}/owner_id/{owner_id}", status_code=status.HTTP_201_CREATED
)
async def create_adoption_request(
    pet_id: PyObjectId,
    owner_id: PyObjectId,
    db: AsyncIOMotorClient = Depends(get_database),
) -> AdoptionDAO:
    return await adoption_controllers.create_adoption_request(
        pet_id=pet_id, owner_id=owner_id, db=db
    )


@router.post(
    "/register/pet_id/{pet_id}/owner_id/{owner_id}", status_code=status.HTTP_201_CREATED
)
async def register_adoption(
    pet_id: PyObjectId,
    owner_id: PyObjectId,
    db: AsyncIOMotorClient = Depends(get_database),
) -> None:
    return await adoption_controllers.register_adoption(
        pet_id=pet_id, owner_id=owner_id, db=db
    )


@router.get("", status_code=status.HTTP_200_OK)
async def read_many(
    db: AsyncIOMotorClient = Depends(get_database),
) -> Iterable[AdoptionDAO]:
    return await adoption_controllers.read_many(db=db)


@router.delete("/pet_id/{pet_id}/owner_id/{owner_id}", status_code=status.HTTP_200_OK)
async def delete_one(
    pet_id: PyObjectId,
    owner_id: PyObjectId,
    db: AsyncIOMotorClient = Depends(get_database),
) -> None:
    return await adoption_controllers.delete_one(
        db=db, pet_id=pet_id, owner_id=owner_id
    )
