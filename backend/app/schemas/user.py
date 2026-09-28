from pydantic import BaseModel, EmailStr, Field, UUID4
from datetime import datetime
from backend.app.models.user import UserRole

class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="nurse_jane")
    email: EmailStr = Field(..., example="jane.doe@hospital.org")
    first_name: str = Field(..., min_length=1, max_length=50, example="Jane")
    last_name: str = Field(..., min_length=1, max_length=50, example="Doe")
    role: UserRole = Field(default=UserRole.JUNIOR_NURSE)

class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=8, max_length=100, example="SecurePassword123!")

class UserResponseSchema(UserBaseSchema):
    user_id: UUID4
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
