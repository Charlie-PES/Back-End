from typing import Optional

from pydantic import ConfigDict, Field
from pymongo import IndexModel

from utils.pyobjectid import PyObjectId
from .schemas import PetIn


class PetDAO(PetIn):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    is_available: bool = True

    @classmethod
    def indexes(cls) -> list[IndexModel]:
        []  # TBD

    @classmethod
    def coll_name(self) -> str:
        return "pets"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str},
    )
