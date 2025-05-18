from typing import Literal
from pydantic import Field

from charlie.applications.common_schemas.base import AppBaseModel
from charlie.utils.pyobjectid import PyObjectId


class PetTraits(AppBaseModel):
    size: Literal["small", "medium", "large"]
    breed: str | None = None
    color: str  # TBD
    fur_type: Literal["short", "medium", "long", "hairless"]
    temperament: Literal["calm", "energetic", "aggressive", "friendly"]
    trained: bool = False


class PetIn(AppBaseModel):
    name: str
    age_months: int = Field(
        ..., ge=0
    )  # with this we make an estimate of the birthday to inner control
    traits: PetTraits
    picture: str  # s3 url


class PetOut(PetIn):
    id: PyObjectId = Field(alias="_id", default=None)


class PetUpdate(AppBaseModel):
    name: str | None = None
    age_months: int | None = None
    traits: PetTraits | None = None
    is_available: bool | None = None
    picture: str | None = None
