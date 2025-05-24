from pydantic import BaseModel
from typing import Optional


class SubjectBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    credits: int = 1
    hours_per_week: int = 1
    classe_id: int


class SubjectCreate(SubjectBase):
    teacher_id: Optional[int] = None


class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None
    hours_per_week: Optional[int] = None
    teacher_id: Optional[int] = None
    classe_id: Optional[int] = None


class SubjectResponse(SubjectBase):
    id: int
    teacher_id: Optional[int] = None

    class Config:
        from_attributes = True
