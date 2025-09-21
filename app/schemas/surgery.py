import datetime
from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional
from typing_extensions import Annotated
from bson import ObjectId

# This function is used to handle ObjectId conversion for responses
PyObjectId = Annotated[str, BeforeValidator(str)]

def calculate_age(birthdate: datetime.date) -> int:
    today = datetime.date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

class SurgeryBase(BaseModel):
    date_time: datetime.datetime
    surgery_type: str
    surgeon_name: str
    patient_name: str
    patient_birthdate: datetime.date

class SurgeryCreate(SurgeryBase):
    """Model for creating a new surgery."""
    pass

class SurgeryInDB(SurgeryBase):
    """Model for a surgery as it is stored in the database."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    patient_age: int

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "date_time": "2025-10-27T10:00:00",
                "surgery_type": "Appendectomy",
                "surgeon_name": "Dr. Smith",
                "patient_name": "John Doe",
                "patient_birthdate": "1990-05-15",
                "patient_age": 35,
            }
        }
