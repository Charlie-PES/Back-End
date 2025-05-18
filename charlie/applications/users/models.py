from typing import Optional

from bson import ObjectId
from pydantic import ConfigDict, Field

from charlie.utils.pyobjectid import PyObjectId
from .schemas import UserIn


class UserDAO(UserIn):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    @classmethod
    def indexes(cls):
        []  # TBD

    @classmethod
    def coll_name(cls) -> str:
        return "users"
