from collections.abc import Iterable
from bson import ObjectId
from applications.pets.schemas import PetIn
from applications.pets.models import PetDAO
from utils.pyobjectid import PyObjectId
from db_operations.operations import create_one as create_one_op
from db_operations.operations import read_one as read_one_op
from db_operations.operations import read_many as read_many_op


from motor.motor_asyncio import AsyncIOMotorClient


async def create_one(pet_in: PetIn, db: AsyncIOMotorClient) -> PetDAO:
    return await create_one_op(entity=PetDAO, data=pet_in, db=db)


async def read_one(pet_id: PyObjectId, db: AsyncIOMotorClient) -> PetDAO:
    return await read_one_op(entity=PetDAO, criteria=ObjectId(pet_id), db=db)


async def read_many(db: AsyncIOMotorClient) -> Iterable[PetDAO]:
    return await read_many_op(entity=PetDAO, db=db)
