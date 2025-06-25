from collections.abc import Iterable
from fastapi import APIRouter, Depends, status, Body, Query
from charlie.utils.pyobjectid import PyObjectId
from charlie.dependencies.database import get_database
from charlie.applications.adoptions.models import AdoptionDAO
from charlie.settings import Settings
from motor.motor_asyncio import AsyncIOMotorClient
from charlie.applications.adoptions import controllers as adoption_controllers

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


@router.get("/compatibility-report", status_code=status.HTTP_200_OK)
async def compatibility_report(
    desired_species: str = Query(...),
    desired_size: str = Query(...),
    desired_sex: str = Query(...),
    accepts_special_needs: bool = Query(...),
    accepts_chronic_disease: bool = Query(...),
    has_other_pets: bool = Query(...),
    has_time: bool = Query(...),
    db: AsyncIOMotorClient = Depends(get_database),
):
    return await adoption_controllers.relatorio_compatibilidade(
        desired_species=desired_species,
        desired_size=desired_size,
        desired_sex=desired_sex,
        accepts_special_needs=accepts_special_needs,
        accepts_chronic_disease=accepts_chronic_disease,
        has_other_pets=has_other_pets,
        has_time=has_time,
        db=db
    )
