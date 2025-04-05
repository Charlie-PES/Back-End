from datetime import date
from pydantic import BaseModel


# WORK IN PROGRESS
class AdoptionIn(BaseModel):
    # pet_id: str
    # adopter_id: str
    # ...
    pass


class AdoptionOut(BaseModel):
    adopter_name: str
    pet_name: str
    adoption_date: date
    # ...
    pass


class AdoptionUpdate(BaseModel):
    # TBD
    pass
