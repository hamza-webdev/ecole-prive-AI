from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..database import Base


class Classe(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    level = Column(String, nullable=False)  # Ex: "6ème", "5ème", "Terminale"
    section = Column(String, nullable=True)  # Ex: "A", "B", "Scientifique"
    academic_year = Column(String, nullable=False)  # Ex: "2023-2024"
    max_students = Column(Integer, default=30)
    description = Column(Text, nullable=True)

    # Relations
    enrollments = relationship("Enrollment", back_populates="classe")
    subjects = relationship("Subject", back_populates="classe")
