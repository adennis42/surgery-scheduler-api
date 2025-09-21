from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas.surgery import SurgeryCreate, SurgeryInDB, calculate_age, SurgeryUpdate
from bson import ObjectId
from typing import List, Optional
import datetime

async def create_new_surgery(db_collection: AsyncIOMotorClient, surgery: SurgeryCreate) -> SurgeryInDB:
    # Calculate age based on birthdate
    patient_age = calculate_age(surgery.patient_birthdate)
    
    # Create the document to be inserted
    surgery_data = surgery.model_dump(by_alias=True)
    surgery_data["patient_age"] = patient_age

    # Convert the patient_birthdate from date to datetime
    surgery_data["patient_birthdate"] = datetime.datetime.combine(
        surgery.patient_birthdate,
        datetime.time.min  # Set the time to midnight
    )
    
    # Insert the new surgery record into the database
    result = await db_collection.insert_one(surgery_data)
    
    # Retrieve the inserted record to get the full data, including the ObjectId
    new_surgery = await db_collection.find_one({"_id": result.inserted_id})
    
    return SurgeryInDB.model_validate(new_surgery)

async def get_all_surgeries(db_client: AsyncIOMotorClient) -> List[SurgeryInDB]:
    # Placeholder for getting all surgeries
    # This will be completed later
    surgeries = await db_client.find().to_list(1000)
    return [SurgeryInDB.model_validate(surgery) for surgery in surgeries]

async def get_surgery_by_id(db_client: AsyncIOMotorClient, surgery_id: str) -> SurgeryInDB:
    # Placeholder for getting a surgery by ID
    # This will be completed later
    surgery = await db_client.find_one({"_id": surgery_id})
    if surgery:
        return SurgeryInDB.model_validate(surgery)
    return None # or raise an exception if not found

async def delete_surgery(db_collection, surgery_id: str) -> bool:
    """Deletes a surgery from the database."""
    try:
        if not ObjectId.is_valid(surgery_id):
            raise ValueError("Invalid surgery ID format")
        
        result = await db_collection.delete_one({"_id": ObjectId(surgery_id)})
        return result.deleted_count == 1
    except Exception:
        return False


async def update_surgery(db_collection, surgery_id: str, surgery_update: SurgeryUpdate) -> Optional[SurgeryInDB]:
    """Updates an existing surgery in the database."""
    try:
        if not ObjectId.is_valid(surgery_id):
            raise ValueError("Invalid surgery ID format")

        # Prepare the update document, converting date to datetime
        update_data = surgery_update.model_dump(exclude_unset=True)
        if "patient_birthdate" in update_data:
            update_data["patient_birthdate"] = datetime.datetime.combine(
                update_data["patient_birthdate"], datetime.time.min
            )
            # Re-calculate age if birthdate is updated
            update_data["patient_age"] = calculate_age(surgery_update.patient_birthdate)

        # Update the document and retrieve the updated version
        update_result = await db_collection.update_one(
            {"_id": ObjectId(surgery_id)},
            {"$set": update_data}
        )
        if update_result.modified_count == 1:
            updated_surgery = await db_collection.find_one({"_id": ObjectId(surgery_id)})
            return SurgeryInDB.model_validate(updated_surgery)
        
        # If no document was modified, check if it existed at all
        existing_surgery = await get_surgery_by_id(db_collection, surgery_id)
        if existing_surgery:
            return existing_surgery # Nothing to update, return existing
        return None # Not found
    except Exception:
        return None
