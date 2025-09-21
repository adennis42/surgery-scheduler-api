from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas.surgery import SurgeryCreate, SurgeryInDB
from app.services.surgery_service import create_new_surgery, get_all_surgeries
from app.core.database import get_db_collection
from typing import List

router = APIRouter()

@router.post(
    "/",
    response_model=SurgeryInDB,
    status_code=status.HTTP_201_CREATED,
    summary="Schedule a new surgery",
)
async def schedule_new_surgery(
    surgery: SurgeryCreate,
    db_collection: AsyncIOMotorClient = Depends(get_db_collection),
):
    """
    Schedules a new surgery and adds it to the list of upcoming surgeries.
    """
    new_surgery = await create_new_surgery(db_collection, surgery)
    return new_surgery

@router.get(
    "/",
    response_model=List[SurgeryInDB],
    status_code=status.HTTP_200_OK,
    summary="View a list of all upcoming surgeries",
)
async def list_all_surgeries(
    db_collection: AsyncIOMotorClient = Depends(get_db_collection),
):
    """
    Retrieves and displays a list of all scheduled surgeries.
    """
    all_surgeries = await get_all_surgeries(db_collection)
    return all_surgeries
