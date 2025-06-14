from charlie.applications.pets.routes import router as pets_router
from charlie.applications.owners.routes import router as owners_router
from charlie.applications.adoptions.routes import router as adoptions_router

from fastapi import FastAPI


def register_routes(app: FastAPI) -> None:
    app.include_router(pets_router, prefix="/v1/pets")
    app.include_router(owners_router, prefix="/v1/owners")
    app.include_router(adoptions_router, prefix="/v1/adoptions")
