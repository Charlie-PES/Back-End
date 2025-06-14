from datetime import date, datetime
from typing import Literal
from pydantic import Field
from typing import Any

from charlie.applications.common_schemas.base import AppBaseModel
from charlie.utils.pyobjectid import PyObjectId


class PetTraits(AppBaseModel):
    size: Literal["small", "medium", "large"]
    breed: str | None = None
    color: str  # TBD
    fur_type: Literal["short", "medium", "long", "hairless"]
    temperament: Literal["calm", "energetic", "aggressive", "friendly"]
    trained: bool = False
    description: str | None = None


class PetIn(AppBaseModel):
    name: str
    birthday_date: datetime
    traits: PetTraits
    picture: str
    is_available: bool = True
    owner_id: PyObjectId
    additional_data: dict[str, Any] | None = None


class PetOut(PetIn):
    id: PyObjectId = Field(alias="_id", default=None)


class PetUpdate(AppBaseModel):
    name: str | None = None
    age_months: int | None = None
    traits: PetTraits | None = None
    is_available: bool | None = None
    picture: str | None = None
