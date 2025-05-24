from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.subject import Subject
from ..models.user import User
from ..schemas.subject import SubjectCreate, SubjectUpdate, SubjectResponse
from ..auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Créer une nouvelle matière."""
    # Vérifier si le code de matière existe déjà
    existing_subject = db.query(Subject).filter(Subject.code == subject.code).first()
    if existing_subject:
        raise HTTPException(
            status_code=400,
            detail="Une matière avec ce code existe déjà"
        )
    
    # Créer la matière
    db_subject = Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


@router.get("/", response_model=List[SubjectResponse])
def read_subjects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lister toutes les matières."""
    subjects = db.query(Subject).offset(skip).limit(limit).all()
    return subjects


@router.get("/{subject_id}", response_model=SubjectResponse)
def read_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtenir une matière par son ID."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Matière non trouvée")
    return subject


@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: int,
    subject_update: SubjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mettre à jour une matière."""
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Matière non trouvée")
    
    # Mettre à jour les champs fournis
    for field, value in subject_update.dict(exclude_unset=True).items():
        setattr(db_subject, field, value)
    
    db.commit()
    db.refresh(db_subject)
    return db_subject


@router.delete("/{subject_id}")
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Supprimer une matière."""
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Matière non trouvée")
    
    db.delete(db_subject)
    db.commit()
    return {"message": "Matière supprimée avec succès"}
