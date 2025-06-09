from applications.pets.routes import router as pets_router
from applications.owners.routes import router as owners_router

from fastapi import FastAPI


def register_routes(app: FastAPI) -> None:
    app.include_router(pets_router, prefix="/v1/pets")
    app.include_router(owners_router, prefix="/v1/owners")
