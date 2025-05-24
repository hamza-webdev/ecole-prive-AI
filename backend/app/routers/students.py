from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.student import Student
from ..models.user import User
from ..schemas.student import StudentCreate, StudentUpdate, StudentResponse
from ..auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Créer un nouveau profil étudiant."""
    # Vérifier si l'utilisateur existe
    user = db.query(User).filter(User.id == student.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Vérifier si le numéro étudiant existe déjà
    existing_student = db.query(Student).filter(Student.student_number == student.student_number).first()
    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Un étudiant avec ce numéro existe déjà"
        )
    
    # Créer le profil étudiant
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.get("/", response_model=List[StudentResponse])
def read_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lister tous les étudiants."""
    students = db.query(Student).offset(skip).limit(limit).all()
    return students


@router.get("/{student_id}", response_model=StudentResponse)
def read_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtenir un étudiant par son ID."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mettre à jour un étudiant."""
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    # Mettre à jour les champs fournis
    for field, value in student_update.dict(exclude_unset=True).items():
        setattr(db_student, field, value)
    
    db.commit()
    db.refresh(db_student)
    return db_student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Supprimer un étudiant."""
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    db.delete(db_student)
    db.commit()
    return {"message": "Étudiant supprimé avec succès"}
