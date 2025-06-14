from pydantic import EmailStr, Field, model_validator
from charlie.applications.owners.utils import VALIDATOR_STRATEGY
from charlie.utils.identifier_validators import IdentifierValidator
from charlie.utils.pyobjectid import PyObjectId
from typing import Any, Literal
from charlie.applications.common_schemas.base import AppBaseModel
from charlie.applications.users.utils import hash_password


class Address(AppBaseModel):
    city: str
    state: str
    neighborhood: str
    street: str
    number: str
    zip_code: str


class OwnerDetails(AppBaseModel):
    description: str | None = None
    additional_data: dict[str, Any] | None = None


class OwnerBase(AppBaseModel):
    type: Literal["tutor", "org"]
    name: str = Field(..., min_length=1, max_length=100)
    pets: list[PyObjectId] = Field(default_factory=list)
    surname: str | None = Field(None, min_length=1, max_length=100)
    address: list[Address] = Field(default_factory=list)
    owner_details: OwnerDetails | None = None
    email: EmailStr
    phone: str
    identifier: str
    picture: str


class OwnerIn(OwnerBase):
    password: str

    def with_hashed_password(self) -> "Owner":
        return self.model_copy(update={"password": hash_password(self.password)})

    @model_validator(mode="after")
    def get_validator(self) -> None:
        validator: IdentifierValidator = VALIDATOR_STRATEGY.get(self.type)
        validator.validate(self.identifier)
        return self


class OwnerOut(OwnerBase):
    id: PyObjectId = Field(alias="_id", default=None)


class LoginRequest(AppBaseModel):
    email: EmailStr
    password: str


class LoginResponse(AppBaseModel):
    message: str
    owner: OwnerOut


class OwnerUpdate(AppBaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    surname: str | None = Field(None, min_length=1, max_length=100)
    owner_details: OwnerDetails | None = None
    picture: str | None = None
