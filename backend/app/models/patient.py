# backend/app/models/patient.py
from database import Base
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Patient(Base):
    __tablename__ = "patients"

    patient_id =  Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        server_default=text("gen_random_uuid()"), 
        index=True
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    sex = Column(String, nullable=False) 
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    historical_visits = relationship("TriageRecord", back_populates="patient_profile")
