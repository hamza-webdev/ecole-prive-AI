from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class StudentBase(BaseModel):
    student_number: str
    date_of_birth: date
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    parent_email: Optional[EmailStr] = None
    emergency_contact: Optional[str] = None
    medical_info: Optional[str] = None


class StudentCreate(StudentBase):
    user_id: int


class StudentUpdate(BaseModel):
    student_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    parent_email: Optional[EmailStr] = None
    emergency_contact: Optional[str] = None
    medical_info: Optional[str] = None


class StudentResponse(StudentBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
