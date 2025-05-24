from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.teacher import Teacher
from ..models.user import User
from ..schemas.teacher import TeacherCreate, TeacherUpdate, TeacherResponse
from ..auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(
    teacher: TeacherCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Créer un nouveau profil enseignant."""
    # Vérifier si l'utilisateur existe
    user = db.query(User).filter(User.id == teacher.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Vérifier si le numéro employé existe déjà
    existing_teacher = db.query(Teacher).filter(Teacher.employee_number == teacher.employee_number).first()
    if existing_teacher:
        raise HTTPException(
            status_code=400,
            detail="Un enseignant avec ce numéro d'employé existe déjà"
        )
    
    # Créer le profil enseignant
    db_teacher = Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


@router.get("/", response_model=List[TeacherResponse])
def read_teachers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lister tous les enseignants."""
    teachers = db.query(Teacher).offset(skip).limit(limit).all()
    return teachers


@router.get("/{teacher_id}", response_model=TeacherResponse)
def read_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtenir un enseignant par son ID."""
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail="Enseignant non trouvé")
    return teacher


@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher(
    teacher_id: int,
    teacher_update: TeacherUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mettre à jour un enseignant."""
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Enseignant non trouvé")
    
    # Mettre à jour les champs fournis
    for field, value in teacher_update.dict(exclude_unset=True).items():
        setattr(db_teacher, field, value)
    
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


@router.delete("/{teacher_id}")
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Supprimer un enseignant."""
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Enseignant non trouvé")
    
    db.delete(db_teacher)
    db.commit()
    return {"message": "Enseignant supprimé avec succès"}
