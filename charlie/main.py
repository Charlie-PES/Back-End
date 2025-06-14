from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from charlie.utils.routes import register_routes
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

    # Configuração do CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Ajuste isso para os domínios permitidos em produção
        allow_credentials=True,
        allow_methods=["*"],  # Permite todos os métodos, incluindo OPTIONS
        allow_headers=["*"],
    )

    register_routes(app)
    return app


app = create_app()


def main() -> None:
    uvicorn.run(
        "charlie.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )


if __name__ == "__main__":
    main()
