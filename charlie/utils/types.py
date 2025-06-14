from typing import Union
from charlie.applications.adoptions.schemas import AdoptionIn, AdoptionUpdate
from charlie.applications.owners.schemas import OwnerIn, OwnerUpdate
from charlie.applications.pets.models import PetDAO
from charlie.applications.pets.schemas import PetIn, PetUpdate
from charlie.applications.users.models import UserDAO
from charlie.applications.owners.models import OwnerDAO
from charlie.applications.adoptions.models import AdoptionDAO
from charlie.applications.users.schemas import UserIn

Entity = Union[PetDAO, UserDAO, OwnerDAO, AdoptionDAO]

EntityIn = Union[PetIn, UserIn, OwnerIn, AdoptionIn]

EntityUpdate = Union[PetUpdate, OwnerUpdate, AdoptionUpdate]
