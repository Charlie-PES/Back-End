from fastapi import HTTPException, status
from charlie.applications.owners.models import OwnerDAO
from charlie.applications.owners.schemas import (
    LoginRequest,
    LoginResponse,
    OwnerOut,
    OwnerIn,
)

from charlie.applications.users.utils import verify_password
from charlie.utils.pyobjectid import PyObjectId
from charlie.db_operations.operations import create_one as create_one_op
from charlie.db_operations.operations import read_one as read_one_op
from charlie.db_operations.operations import read_many as read_many_op


from motor.motor_asyncio import AsyncIOMotorClient


async def register_owner(owner_in: OwnerIn, db: AsyncIOMotorClient) -> OwnerOut:
    owner = await create_one_op(
        entity=OwnerDAO, data=owner_in.with_hashed_password(), db=db
    )
    return OwnerOut(**owner.model_dump(by_alias=True))


async def login(login_data: LoginRequest, db: AsyncIOMotorClient) -> LoginResponse:
    criteria = {"email": login_data.email}
    owner: OwnerDAO = await read_one_op(entity=OwnerDAO, criteria=criteria, db=db)

    if not verify_password(login_data.password, owner.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return LoginResponse(
        owner=OwnerOut(**owner.model_dump(by_alias=True)), message="Login successful"
    )


async def read_one(owner_id: PyObjectId, db: AsyncIOMotorClient) -> OwnerOut:
    owner = await read_one_op(entity=OwnerDAO, criteria=owner_id, db=db)
    return OwnerOut(**owner.model_dump(by_alias=True))


async def read_many(db: AsyncIOMotorClient) -> list[OwnerDAO]:
    return await read_many_op(entity=OwnerDAO, db=db)
