from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response # Added Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.student import Student
from ..models.user import User
from ..schemas.student import StudentCreate, StudentUpdate, StudentResponse
from ..auth import get_current_active_user

router = APIRouter()

# --- Utility Dependency ---
def get_student_or_404(student_id: int, db: Session = Depends(get_db)) -> Student:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Étudiant non trouvé")
    return student

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
    student: Student = Depends(get_student_or_404),
    current_user: User = Depends(get_current_active_user) # Keep for auth, db is in get_student_or_404
):
    """Obtenir un étudiant par son ID."""
    # student_id is implicitly handled by Depends(get_student_or_404)
    # db session is also handled by the dependency
    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_update: StudentUpdate, # student_id is implicit now
    student: Student = Depends(get_student_or_404),
    db: Session = Depends(get_db), # Still need db for commit
    current_user: User = Depends(get_current_active_user)
):
    """Mettre à jour un étudiant."""
    # student object is already fetched by get_student_or_404
    
    # Mettre à jour les champs fournis
    for field, value in student_update.dict(exclude_unset=True).items():
        setattr(student, field, value) # Use student from dependency
    
    db.add(student) # Add to session before commit if changes were made
    db.commit()
    db.refresh(student)
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student: Student = Depends(get_student_or_404), # student_id is implicit
    db: Session = Depends(get_db), # Still need db for commit
    current_user: User = Depends(get_current_active_user) # Keep this for auth
):
    """Supprimer un étudiant."""
    # student object is already fetched by get_student_or_404
    
    db.delete(student) # Use student from dependency
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
