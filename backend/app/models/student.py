from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    student_number = Column(String, unique=True, index=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    parent_name = Column(String, nullable=True)
    parent_phone = Column(String, nullable=True)
    parent_email = Column(String, nullable=True)
    emergency_contact = Column(String, nullable=True)
    medical_info = Column(String, nullable=True)

    # Relations
    user = relationship("User", back_populates="student_profile")
    enrollments = relationship("Enrollment", back_populates="student")
