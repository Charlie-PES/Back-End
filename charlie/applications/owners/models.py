from bson import ObjectId
from pydantic import ConfigDict
from pymongo import IndexModel


from .schemas import OwnerIn


class OwnerDAO(OwnerIn):
    # TBD

    @classmethod
    def indexes(cls) -> list[IndexModel]:
        [IndexModel("email", unique=True)]

    @classmethod
    def coll_name(cls) -> str:
        return "owners"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
