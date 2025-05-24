#!/usr/bin/env python3
"""
Script pour vider la base de données
"""

from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models.user import User
from .models.student import Student
from .models.teacher import Teacher
from .models.classe import Classe
from .models.subject import Subject
from .models.enrollment import Enrollment


def clear_database():
    """Vider toutes les tables de la base de données."""
    print("🗑️  Début du nettoyage de la base de données...")
    
    # Créer une session
    db = SessionLocal()
    
    try:
        # Supprimer dans l'ordre inverse des dépendances
        print("   Suppression des inscriptions...")
        db.query(Enrollment).delete()
        
        print("   Suppression des matières...")
        db.query(Subject).delete()
        
        print("   Suppression des profils étudiants...")
        db.query(Student).delete()
        
        print("   Suppression des profils enseignants...")
        db.query(Teacher).delete()
        
        print("   Suppression des classes...")
        db.query(Classe).delete()
        
        print("   Suppression des utilisateurs...")
        db.query(User).delete()
        
        # Valider les suppressions
        db.commit()
        
        print("✅ Base de données vidée avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    clear_database()
