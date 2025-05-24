from pydantic import BaseModel
from typing import Optional


class ClasseBase(BaseModel):
    name: str
    level: str
    section: Optional[str] = None
    academic_year: str
    max_students: int = 30
    description: Optional[str] = None


class ClasseCreate(ClasseBase):
    pass


class ClasseUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[str] = None
    section: Optional[str] = None
    academic_year: Optional[str] = None
    max_students: Optional[int] = None
    description: Optional[str] = None


class ClasseResponse(ClasseBase):
    id: int

    class Config:
        from_attributes = True
