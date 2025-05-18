from bson import ObjectId
from typing import Optional

from pydantic import Field

from charlie.applications.common_schemas.base import AppBaseModel
from charlie.applications.users.utils import hash_password
from charlie.utils.pyobjectid import PyObjectId


class UserIn(AppBaseModel):
    username: str
    cpf: str
    email: str
    password: str
    tutor: bool
    adopter: bool

    def with_hashed_password(self) -> "UserIn":
        return self.model_copy(update={"password": hash_password(self.password)})


class UserOut(AppBaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    cpf: str
    email: str
    tutor: bool
    adopter: bool


class LoginRequest(AppBaseModel):
    username: str
    password: str


class LoginResponse(AppBaseModel):
    message: str
    user: UserOut
