from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    employee_number = Column(String, unique=True, index=True, nullable=False)
    hire_date = Column(Date, nullable=False)
    specialization = Column(String, nullable=True)
    qualifications = Column(Text, nullable=True)
    salary = Column(Integer, nullable=True)  # En centimes pour éviter les problèmes de float

    # Relations
    user = relationship("User", back_populates="teacher_profile")
    subjects = relationship("Subject", back_populates="teacher")
