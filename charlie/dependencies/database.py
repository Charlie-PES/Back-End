from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from settings import Settings

settings = Settings()


def start_db(app: FastAPI) -> None:
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URI)
    app.database = app.mongodb_client[settings.DB_NAME]
    print("Connected to MongoDB (motor)")


def close_db(app: FastAPI) -> None:
    app.mongodb_client.close()
    print("Disconnected from MongoD")
