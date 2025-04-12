from fastapi import FastAPI
import uvicorn


from utils.routes import register_routes
from dependencies.database import start_db, close_db
from settings import Settings
from contextlib import asynccontextmanager

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_db(app)
    yield
    close_db(app)


def create_app() -> FastAPI:
    app = FastAPI(title="Charlie API", lifespan=lifespan)
    register_routes(app)
    return app


app = create_app()


def main() -> None:
    uvicorn.run(
        "main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD
    )


if __name__ == "__main__":
    main()
