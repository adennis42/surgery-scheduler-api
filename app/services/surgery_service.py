from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas.surgery import SurgeryCreate, SurgeryInDB, calculate_age
from typing import List
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
