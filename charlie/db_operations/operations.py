from collections.abc import AsyncIterable
from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from db_operations.utils import DatabaseError, DocumentNotFoundError
from pymongo.errors import DuplicateKeyError, PyMongoError
from utils.types import Entity, EntityIn
from typing import Any
from typing import Type


async def create_one(
    entity: Type[Entity], data: EntityIn, db: AsyncIOMotorClient
) -> Entity:
    collection_name = entity.coll_name()
    collection: AsyncIOMotorCollection = db[collection_name]
    document_data = data.model_dump(by_alias=True)
    try:
        result = await collection.insert_one(document_data)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Document with the same _id already exists in {collection_name} collection.",
        )
    except PyMongoError as e:
        raise DatabaseError(
            f"An error occurred while inserting the document into {collection_name}: {str(e)}"
        )

    document_with_id = {**document_data, "_id": result.inserted_id}
    return entity.model_validate(document_with_id)


async def read_one(
    entity: Type[Entity], criteria: dict[str, Any] | ObjectId, db: AsyncIOMotorClient
) -> Entity:
    if isinstance(criteria, ObjectId):
        criteria = {"_id": criteria}
    collection_name = entity.coll_name()
    collection: AsyncIOMotorCollection = db[collection_name]
    try:
        result = await collection.find_one(criteria)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document not found in {collection_name} collection with criteria: {criteria}",
            )

    except PyMongoError as e:
        raise DatabaseError(f"Error while accessing the database: {str(e)}")

    return entity.model_validate(result)


async def read_many(
    entity: Type[Entity], db: AsyncIOMotorClient
) -> AsyncIterable[Entity]:
    collection_name = entity.coll_name()
    collection: AsyncIOMotorCollection = db[collection_name]
    documents = await collection.find().to_list(length=None)
    return [entity.model_validate(doc) for doc in documents]


async def delete_one(
    entity: Type[Entity], criteria: dict[str, Any] | ObjectId, db: AsyncIOMotorClient
) -> None:
    if isinstance(criteria, ObjectId):
        criteria = {"_id": criteria}
    collection_name = entity.coll_name()
    collection: AsyncIOMotorCollection = db[collection_name]
    try:
        result = await collection.delete_one(criteria)
        if not result.deleted_count:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document not found in {collection_name} collection with criteria: {criteria}",
            )
    except PyMongoError as e:
        raise DatabaseError(f"Error while accessing the database: {str(e)}")


# todo: implement update_one
async def update_one() -> None:
    pass
