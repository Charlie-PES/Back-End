import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from charlie.settings import Settings

@pytest_asyncio.fixture
async def db_client() -> AsyncIOMotorDatabase:
    """Fixture para criar um cliente do MongoDB para testes.
    
    Returns:
        AsyncIOMotorDatabase: Cliente do banco de dados para testes
    """
    settings = Settings()
    client = AsyncIOMotorClient(settings.DB_URI)
    db = client[settings.DB_NAME]
    yield db
    client.close()  # Não é necessário await pois close() não é uma corotina
