from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

def get_db_collection(request: Request) -> AsyncIOMotorClient:
    """
    Returns the MongoDB collection for surgeries.
    """
    return request.app.mongodb[settings.DB_NAME]["surgeries"]
