from fastapi import APIRouter
from settings import Settings


settings = Settings()
router = APIRouter(prefix="/pets", tags=["pets"])


# POST api/pet -> demands PetIn, return PetDAO

# GET api/pet -> return Iterable[PetDAO]

# GET api/pet/id -> return PetDAO

# PATCH api/pet/id -> demands PetUpdate, return None

# DELETE api/pet/id -> return None
