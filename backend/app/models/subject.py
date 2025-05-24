from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    credits = Column(Integer, default=1)
    hours_per_week = Column(Integer, default=1)
    
    # Relations
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)
    classe_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    
    teacher = relationship("Teacher", back_populates="subjects")
    classe = relationship("Classe", back_populates="subjects")
