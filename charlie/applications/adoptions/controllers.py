from collections.abc import Iterable
from fastapi import HTTPException
from charlie.applications.adoptions.models import AdoptionDAO
from charlie.applications.pets.models import PetDAO
from charlie.applications.owners.models import OwnerDAO
from charlie.applications.adoptions.schemas import AdoptionIn
from charlie.utils.pyobjectid import PyObjectId
from charlie.db_operations.operations import (
    create_one as create_one_op,
    read_one as read_one_op,
    read_many as read_many_op,
    delete_one as delete_one_op,
    update_one as update_one_op,
)
from charlie.applications.users.models import UserDAO
from charlie.applications.adoptions.compatibility import calcular_compatibilidade

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


async def relatorio_compatibilidade(
    desired_species: str,
    desired_size: str,
    desired_sex: str,
    accepts_special_needs: bool,
    accepts_chronic_disease: bool,
    has_other_pets: bool,
    has_time: bool,
    db
):
    # Monta o dicionário de preferências do adotante
    adotante_prefs = {
        "desired_species": desired_species,
        "desired_size": desired_size,
        "desired_sex": desired_sex,
        "accepts_special_needs": accepts_special_needs,
        "accepts_chronic_disease": accepts_chronic_disease,
        "has_other_pets": has_other_pets,
        "has_time": has_time
    }
    pets = await read_many_op(entity=PetDAO, db=db, filters={"is_available": True})
    relatorio = []
    for pet in pets:
        score = calcular_compatibilidade(adotante_prefs, pet.model_dump())
        if score != float('-inf'):
            relatorio.append({
                "pet_id": str(pet.id),
                "pet_name": getattr(pet, 'name', None),
                "score": score
            })
    relatorio.sort(key=lambda x: x["score"])
    return relatorio
