from pydantic import BaseModel,ConfigDict, Field, field_validator, UUID4
from datetime import datetime
from typing import Dict, Any


class TriageRecordRequestSchema(BaseModel):
    patient_id: UUID4
    
    systolic_bp: float = Field(..., ge=20.0, le=300.0, description="Systolic BP (mmHg)")
    diastolic_bp: float = Field(..., ge=10.0, le=200.0, description="Diastolic BP (mmHg)")
    heart_rate: float = Field(..., ge=30.0, le=250.0, description="Heart Rate (BPM)")
    respiratory_rate: float = Field(..., ge=4.0, le=60.0, description="Respiratory Rate (breaths/min)")
    temperature_c: float = Field(..., ge=25.0, le=45.0, description="Core Temperature (Celsius)")
    spo2: float = Field(..., ge=40.0, le=100.0, description="Peripheral Oxygen Saturation (%)")
    
    age: int = Field(..., ge=0, le=125)
    gcs_total: int = Field(..., ge=3, le=15, description="Glasgow Coma Scale Total")
    pain_score: int = Field(..., ge=0, le=10, description="Pain Score (handles fixed -1 transformations via frontend)")
    
    arrival_mode: str = Field(..., example="ambulance")
    arrival_day: str = Field(..., example="Monday")
    arrival_hour: int = Field(..., ge=0, le=23)
    
    clinical_history_json: Dict[str, Any] = Field(
        ..., 
        example={"hx_diabetes_type2": 1.0, "hx_asthma": 0.0, "hx_ckd": 1.0}
    )
    
    chief_complaint_raw: str = Field(..., min_length=2, max_length=500, example="Crushing chest pain radiating to left arm")

    @field_validator("spo2")
    @classmethod
    def validate_spo2_sanity_ceiling(cls, value: float) -> float:
        if value > 100.0:
            raise ValueError("Oxygen saturation levels cannot physically cross the 100% threshold.")
        return value

class TriageRecordResponseSchema(BaseModel):
    record_id: UUID4
    patient_id: UUID4
    predicted_target_label: int
    predicted_esi_level: int
    confidence_score: float
    shap_explanations_json: Dict[str, Any]
    created_at: datetime
    recorded_by_user_id: int

    class Config:
        from_attributes = True
