from charlie.utils.pyobjectid import PyObjectId
from .schemas import OwnerIn

from typing import Optional
from bson import ObjectId
from pydantic import ConfigDict, Field
from pymongo import IndexModel


class OwnerDAO(OwnerIn):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    @classmethod
    def indexes(cls) -> list[IndexModel]:
        [IndexModel("email", unique=True), IndexModel("identifier", unique=True)]

    @classmethod
    def coll_name(cls) -> str:
        return "owners"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
