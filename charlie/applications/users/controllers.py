from fastapi import HTTPException, status
from charlie.applications.users.models import UserDAO
from charlie.applications.users.schemas import (
    LoginRequest,
    LoginResponse,
    UserIn,
    UserOut,
)

from charlie.applications.users.utils import verify_password
from charlie.utils.pyobjectid import PyObjectId
from db_operations.operations import create_one as create_one_op
from db_operations.operations import read_one as read_one_op


from motor.motor_asyncio import AsyncIOMotorClient


async def register_user(user_in: UserIn, db: AsyncIOMotorClient) -> UserOut:
    user = await create_one_op(
        entity=UserDAO, data=user_in.with_hashed_password(), db=db
    )
    return UserOut(**user.model_dump(by_alias=True))


async def login(login_data: LoginRequest, db: AsyncIOMotorClient) -> LoginResponse:
    criteria = {"username": login_data.username}
    user: UserDAO = await read_one_op(entity=UserDAO, criteria=criteria, db=db)

    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return LoginResponse(
        user=UserOut(**user.model_dump(by_alias=True)), message="Login successful"
    )


async def read_one(user_id: PyObjectId, db: AsyncIOMotorClient) -> UserOut:
    user = await read_one_op(entity=UserDAO, criteria=user_id, db=db)
    return UserOut(**user.model_dump(by_alias=True))
