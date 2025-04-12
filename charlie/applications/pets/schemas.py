from typing import Literal
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class PetTraits(BaseModel):
    size: Literal["small", "medium", "large"]
    breed: str | None = None
    color: str  # TBD
    fur_type: Literal["short", "medium", "long", "hairless"]
    temperament: Literal["calm", "energetic", "aggressive", "friendly"]
    trained: bool = False


class PetIn(BaseModel):
    name: str
    age_months: int = Field(
        ..., ge=0
    )  # with this we make an estimate of the birthday to inner control
    traits: PetTraits
    picture: str  # s3 url


class PetOut(PetIn):
    id: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )


class PetUpdate(BaseModel):
    name: str | None = None
    age_months: int | None = None
    traits: PetTraits | None = None
    is_available: bool | None = None
    picture: str | None = None
