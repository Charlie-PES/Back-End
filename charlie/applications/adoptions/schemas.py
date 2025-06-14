from typing import Literal
from charlie.applications.common_schemas.base import AppBaseModel
from charlie.utils.pyobjectid import PyObjectId


class AdoptionIn(AppBaseModel):
    owner_id: PyObjectId
    pet_id: PyObjectId
    status: Literal["IN_PROGRESS", "ADOPTED"] = "IN_PROGRESS"


# wip
class AdoptionUpdate(AppBaseModel):
    pass
