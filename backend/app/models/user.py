from database import Base
import enum
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class UserRole(str, enum.Enum):
    JUNIOR_NURSE = "junior_nurse"
    ATTENDING_PHYSICIAN = "attending_physician"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        server_default=text("gen_random_uuid()"), 
        index=True
    )
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.JUNIOR_NURSE)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    triage_records = relationship("TriageRecord", back_populates="recorder")
