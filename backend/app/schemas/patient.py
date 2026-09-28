from pydantic import BaseModel, Field, UUID4
from datetime import datetime

class PatientBaseSchema(BaseModel):
    patient_id: UUID4 
    first_name: str = Field(..., min_length=1, max_length=50, example="John")
    last_name: str = Field(..., min_length=1, max_length=50, example="Smith")
    sex: str = Field(..., min_length=1, max_length=10, example="M") 

class PatientCreateSchema(PatientBaseSchema):
    pass

class PatientResponseSchema(PatientBaseSchema):
    created_at: datetime

    class Config:
        from_attributes = True
