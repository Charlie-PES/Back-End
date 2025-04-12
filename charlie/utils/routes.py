from applications.users.routes import router as user_router
from applications.pets.routes import router as pets_router
from fastapi import FastAPI


def register_routes(app: FastAPI) -> None:
    app.include_router(pets_router, prefix="/v1/pets")
    app.include_router(user_router, prefix="/v1/users")
