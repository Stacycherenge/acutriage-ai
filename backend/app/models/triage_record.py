# backend/app/models/triage_record.py
from database import Base
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Float,
    JSON,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class TriageRecord(Base):
    __tablename__ = "triage_records"

    record_id = Column(Integer, primary_key=True, index=True)
    
    # Relational linking to the master Patient registry index
    patient_id = Column(UUID(as_uuid=True),, ForeignKey("patients.patient_id"), nullable=False, index=True)
    # 1. Base Real-Time Physiological Vitals Ingestion Array
    systolic_bp = Column(Float, nullable=False)
    diastolic_bp = Column(Float, nullable=False)
    heart_rate = Column(Float, nullable=False)
    respiratory_rate = Column(Float, nullable=False)
    temperature_c = Column(Float, nullable=False)
    spo2 = Column(Float, nullable=False)
    
    # 2. Acute In-Take Metrics
    age = Column(Integer, nullable=False)
    gcs_total = Column(Integer, nullable=False)
    pain_score = Column(Integer, nullable=False)
    
    # 3. Cyclical and Methodological Metadata Tracker
    arrival_mode = Column(String, nullable=False)
    arrival_day = Column(String, nullable=False)
    arrival_hour = Column(Integer, nullable=False)
    
    # 4. Advanced Clinical History Vault (Houses programmatic 'hx_' boolean checks)
    clinical_history_json = Column(JSON, nullable=False)
    
    # 5. Natural Language Processing Text Layer (Raw nurse notes inputs)
    chief_complaint_raw = Column(String, nullable=False)
    
    # =====================================================================
    # 🧠 DEEP LEARNING MODEL PREDICTIVE METRICS ARTIFACTS
    # =====================================================================
    # Zero-indexed target assignment for PyTorch cross-entropy compliance (0-4)
    predicted_target_label = Column(Integer, nullable=False)
    # Standard ESI priority tier score returned to clinical user (1-5)
    predicted_esi_level = Column(Integer, nullable=False)
    confidence_score = Column(Float, nullable=False)
    # Stores game-theoretic SHAP vectors to drive frontend UI attribution charts
    shap_explanations_json = Column(JSON, nullable=False)
    
    # 6. Administrative Compliance Audits
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Foreign key tracking who logged the record
    recorded_by_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # Back-population mapping vectors linking all three entities relationally
    patient_profile = relationship("Patient", back_populates="historical_visits")
    recorder = relationship("User", back_populates="triage_records")
