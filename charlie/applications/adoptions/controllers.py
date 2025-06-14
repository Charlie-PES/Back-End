from collections.abc import Iterable
from fastapi import HTTPException
from applications.adoptions.models import AdoptionDAO
from applications.pets.models import PetDAO
from applications.owners.models import OwnerDAO
from charlie.applications.adoptions.schemas import AdoptionIn
from utils.pyobjectid import PyObjectId
from db_operations.operations import (
    create_one as create_one_op,
    read_one as read_one_op,
    read_many as read_many_op,
    delete_one as delete_one_op,
    update_one as update_one_op,
)

from motor.motor_asyncio import AsyncIOMotorClient


async def create_adoption_request(
    pet_id: PyObjectId, owner_id: PyObjectId, db: AsyncIOMotorClient
) -> AdoptionDAO:
    pet: PetDAO = await read_one_op(entity=PetDAO, criteria=pet_id, db=db)
    if not pet.is_available:
        raise HTTPException(
            status_code=400, detail="Pet is not available for adoption."
        )

    await read_one_op(entity=OwnerDAO, criteria=owner_id, db=db)
    adoption_in = AdoptionIn(pet_id=pet_id, owner_id=owner_id)
    return await create_one_op(entity=AdoptionDAO, data=adoption_in, db=db)


async def register_adoption(
    pet_id: PyObjectId, owner_id: PyObjectId, db: AsyncIOMotorClient
) -> None:
    pet: PetDAO = await read_one_op(entity=PetDAO, criteria=pet_id, db=db)
    if not pet.is_available:
        raise HTTPException(
            status_code=400, detail="Pet is not available for adoption."
        )

    await read_one_op(entity=OwnerDAO, criteria=owner_id, db=db)
    await read_one_op(entity=PetDAO, criteria=pet_id, db=db)

    await update_one_op(
        entity=AdoptionDAO,
        criteria={"pet_id": pet_id, "owner_id": owner_id},
        update_data={"$set": {"status": "ADOPTED"}},
        db=db,
    )

    await update_one_op(
        entity=PetDAO,
        criteria=pet_id,
        update_data={"$set": {"is_available": False}},
        db=db,
    )

    await update_one_op(
        entity=OwnerDAO,
        criteria=owner_id,
        update_data={"$push": {"pets": pet_id}},
        db=db,
    )


async def read_many(db: AsyncIOMotorClient) -> Iterable[PetDAO]:
    return await read_many_op(entity=AdoptionDAO, db=db)


async def delete_one(
    pet_id: PyObjectId, owner_id: PyObjectId, db: AsyncIOMotorClient
) -> None:
    await read_one_op(entity=PetDAO, criteria=pet_id, db=db)
    await read_one_op(entity=OwnerDAO, criteria=owner_id, db=db)

    await delete_one_op(
        entity=AdoptionDAO,
        criteria={"pet_id": pet_id, "owner_id": owner_id},
        db=db,
    )

    await update_one_op(
        entity=PetDAO,
        criteria=pet_id,
        update_data={"$set": {"is_available": True}},
        db=db,
    )

    await update_one_op(
        entity=OwnerDAO,
        criteria=owner_id,
        update_data={"$pull": {"pets": pet_id}},
        db=db,
    )
