from .user import UserCreate, UserUpdate, UserResponse, UserLogin, Token
from .student import StudentCreate, StudentUpdate, StudentResponse
from .teacher import TeacherCreate, TeacherUpdate, TeacherResponse
from .classe import ClasseCreate, ClasseUpdate, ClasseResponse
from .subject import SubjectCreate, SubjectUpdate, SubjectResponse

__all__ = [
    "UserCreate", "UserUpdate", "UserResponse", "UserLogin", "Token",
    "StudentCreate", "StudentUpdate", "StudentResponse",
    "TeacherCreate", "TeacherUpdate", "TeacherResponse",
    "ClasseCreate", "ClasseUpdate", "ClasseResponse",
    "SubjectCreate", "SubjectUpdate", "SubjectResponse"
]
