from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.classe import Classe
from ..models.user import User
from ..schemas.classe import ClasseCreate, ClasseUpdate, ClasseResponse
from ..auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=ClasseResponse, status_code=status.HTTP_201_CREATED)
def create_classe(
    classe: ClasseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Créer une nouvelle classe."""
    # Vérifier si le nom de classe existe déjà
    existing_classe = db.query(Classe).filter(Classe.name == classe.name).first()
    if existing_classe:
        raise HTTPException(
            status_code=400,
            detail="Une classe avec ce nom existe déjà"
        )
    
    # Créer la classe
    db_classe = Classe(**classe.dict())
    db.add(db_classe)
    db.commit()
    db.refresh(db_classe)
    return db_classe


@router.get("/", response_model=List[ClasseResponse])
def read_classes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lister toutes les classes."""
    classes = db.query(Classe).offset(skip).limit(limit).all()
    return classes


@router.get("/{classe_id}", response_model=ClasseResponse)
def read_classe(
    classe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtenir une classe par son ID."""
    classe = db.query(Classe).filter(Classe.id == classe_id).first()
    if classe is None:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    return classe


@router.put("/{classe_id}", response_model=ClasseResponse)
def update_classe(
    classe_id: int,
    classe_update: ClasseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mettre à jour une classe."""
    db_classe = db.query(Classe).filter(Classe.id == classe_id).first()
    if db_classe is None:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    
    # Mettre à jour les champs fournis
    for field, value in classe_update.dict(exclude_unset=True).items():
        setattr(db_classe, field, value)
    
    db.commit()
    db.refresh(db_classe)
    return db_classe


@router.delete("/{classe_id}")
def delete_classe(
    classe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Supprimer une classe."""
    db_classe = db.query(Classe).filter(Classe.id == classe_id).first()
    if db_classe is None:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    
    db.delete(db_classe)
    db.commit()
    return {"message": "Classe supprimée avec succès"}
