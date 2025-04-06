from fastapi import FastAPI
import uvicorn
from charlie.applications.users.routes import router as user_router
from charlie.dependencies.database import start_db, close_db
from charlie.settings import Settings
from contextlib import asynccontextmanager

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_db(app)
    yield
    close_db(app)


def create_app() -> FastAPI:
    app = FastAPI(title="Charlie API", lifespan=lifespan)
    app.include_router(user_router, prefix="/v1")
    return app


app = create_app()


def main():
    uvicorn.run(
        "main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD
    )


if __name__ == "__main__":
    main()
