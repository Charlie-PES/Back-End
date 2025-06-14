from typing import Literal, Optional

from pydantic import Field
from pymongo import IndexModel

from charlie.utils.pyobjectid import PyObjectId
from .schemas import AdoptionIn


class AdoptionDAO(AdoptionIn):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    @classmethod
    def indexes(cls) -> list[IndexModel]:
        []  # TBD

    @classmethod
    def coll_name(self) -> str:
        return "adoptions"
