from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient
from charlie.settings import Settings

settings = Settings()


def start_db(app: FastAPI) -> None:
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URI)
    app.database = app.mongodb_client[settings.DB_NAME]
    print("✅ Connected to MongoDB (motor)")


def close_db(app: FastAPI) -> None:
    app.mongodb_client.close()
    print("❌ Disconnected from MongoDB")


async def get_database(request: Request):
    return request.app.database
