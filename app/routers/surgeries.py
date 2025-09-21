from fastapi import APIRouter, Depends, status, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas.surgery import SurgeryCreate, SurgeryInDB
from app.services.surgery_service import create_new_surgery, get_all_surgeries, delete_surgery, update_surgery
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

@router.delete(
    "/{surgery_id}",
    status_code=status.HTTP_200_OK,
    summary="Cancel a scheduled surgery",
)
async def cancel_surgery(
    surgery_id: str,
    db_collection: AsyncIOMotorClient = Depends(get_db_collection),
):
    """
    Cancels an existing surgery from the schedule.
    """
    success = await delete_surgery(db_collection, surgery_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Surgery with id {surgery_id} not found",
        )
    # Return 204 No Content on successful deletion
    return {"message": f"Surgery with id {surgery_id} successfully cancelled."}

@router.put(
    "/{surgery_id}",
    response_model=SurgeryInDB,
    status_code=status.HTTP_200_OK,
    summary="Update details of a scheduled surgery",
)
async def modify_surgery(
    surgery_id: str,
    surgery: SurgeryCreate,
    db_collection: AsyncIOMotorClient = Depends(get_db_collection),
):
    """
    Updates the details of a scheduled surgery by its ID.
    """
    updated_surgery = await update_surgery(db_collection, surgery_id, surgery)
    if not updated_surgery:
        raise HTTPException(status_code=404, detail="Surgery not found")
    return updated_surgery