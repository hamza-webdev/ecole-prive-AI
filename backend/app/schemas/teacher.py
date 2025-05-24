from pydantic import BaseModel
from typing import Optional
from datetime import date


class TeacherBase(BaseModel):
    employee_number: str
    hire_date: date
    specialization: Optional[str] = None
    qualifications: Optional[str] = None
    salary: Optional[int] = None


class TeacherCreate(TeacherBase):
    user_id: int


class TeacherUpdate(BaseModel):
    employee_number: Optional[str] = None
    hire_date: Optional[date] = None
    specialization: Optional[str] = None
    qualifications: Optional[str] = None
    salary: Optional[int] = None


class TeacherResponse(TeacherBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
