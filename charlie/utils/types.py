from typing import Union
from applications.adoptions.schemas import AdoptionIn
from applications.owners.schemas import OwnerIn
from applications.pets.models import PetDAO
from applications.pets.schemas import PetIn
from applications.users.models import UserDAO
from applications.owners.models import OwnerDAO
from applications.adoptions.models import AdoptionDAO
from applications.users.schemas import UserIn

Entity = Union[PetDAO, UserDAO, OwnerDAO, AdoptionDAO]

EntityIn = Union[PetIn, UserIn, OwnerIn, AdoptionIn]
