#!/usr/bin/env python3
"""
Script de génération de données fictives pour l'application École Privée
Utilise Faker pour créer des données réalistes de test
"""

import random
from datetime import date, datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models.user import User, UserRole
from .models.student import Student
from .models.teacher import Teacher
from .models.classe import Classe
from .models.subject import Subject
from .models.enrollment import Enrollment, EnrollmentStatus
from .auth import get_password_hash

# Configuration Faker en français
fake = Faker('fr_FR')
Faker.seed(42)  # Pour des résultats reproductibles


def create_admin_user(db: Session) -> User:
    """Créer un utilisateur administrateur par défaut."""
    admin = User(
        email="admin@ecole-prive.fr",
        username="admin",
        first_name="Administrateur",
        last_name="Système",
        hashed_password=get_password_hash("admin123"),
        role=UserRole.ADMIN,
        phone="01.23.45.67.89",
        address="123 Rue de l'École, 75001 Paris",
        is_active=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print(f"✅ Administrateur créé: {admin.email}")
    return admin


def create_fake_users(db: Session, count: int, role: UserRole) -> list[User]:
    """Créer des utilisateurs fictifs."""
    users = []
    
    for i in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}.{last_name.lower()}{i+1}"
        email = f"{username}@ecole-prive.fr"
        
        user = User(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            hashed_password=get_password_hash("password123"),
            role=role,
            phone=fake.phone_number(),
            address=fake.address(),
            is_active=True
        )
        
        db.add(user)
        users.append(user)
    
    db.commit()
    for user in users:
        db.refresh(user)
    
    print(f"✅ {count} utilisateurs {role.value} créés")
    return users


def create_fake_teachers(db: Session, teacher_users: list[User]) -> list[Teacher]:
    """Créer des profils enseignants fictifs."""
    teachers = []
    specializations = [
        "Mathématiques", "Français", "Histoire-Géographie", "Sciences Physiques",
        "Sciences de la Vie et de la Terre", "Anglais", "Espagnol", "Allemand",
        "Éducation Physique et Sportive", "Arts Plastiques", "Musique", "Philosophie",
        "Économie", "Informatique", "Technologie"
    ]
    
    for i, user in enumerate(teacher_users):
        teacher = Teacher(
            user_id=user.id,
            employee_number=f"ENS{2024}{i+1:03d}",
            hire_date=fake.date_between(start_date='-10y', end_date='today'),
            specialization=random.choice(specializations),
            qualifications=fake.text(max_nb_chars=200),
            salary=random.randint(250000, 450000)  # En centimes (2500€ à 4500€)
        )
        
        db.add(teacher)
        teachers.append(teacher)
    
    db.commit()
    for teacher in teachers:
        db.refresh(teacher)
    
    print(f"✅ {len(teachers)} profils enseignants créés")
    return teachers


def create_fake_students(db: Session, student_users: list[User]) -> list[Student]:
    """Créer des profils étudiants fictifs."""
    students = []
    
    for i, user in enumerate(student_users):
        # Date de naissance entre 6 et 18 ans
        birth_date = fake.date_between(start_date='-18y', end_date='-6y')
        
        student = Student(
            user_id=user.id,
            student_number=f"ETU{2024}{i+1:04d}",
            date_of_birth=birth_date,
            parent_name=fake.name(),
            parent_phone=fake.phone_number(),
            parent_email=fake.email(),
            emergency_contact=fake.phone_number(),
            medical_info=fake.text(max_nb_chars=100) if random.choice([True, False]) else None
        )
        
        db.add(student)
        students.append(student)
    
    db.commit()
    for student in students:
        db.refresh(student)
    
    print(f"✅ {len(students)} profils étudiants créés")
    return students


def create_fake_classes(db: Session) -> list[Classe]:
    """Créer des classes fictives."""
    classes_data = [
        # Primaire
        ("CP A", "CP", "A", 25),
        ("CP B", "CP", "B", 25),
        ("CE1 A", "CE1", "A", 25),
        ("CE1 B", "CE1", "B", 25),
        ("CE2 A", "CE2", "A", 25),
        ("CM1 A", "CM1", "A", 25),
        ("CM2 A", "CM2", "A", 25),
        
        # Collège
        ("6ème A", "6ème", "A", 28),
        ("6ème B", "6ème", "B", 28),
        ("5ème A", "5ème", "A", 28),
        ("5ème B", "5ème", "B", 28),
        ("4ème A", "4ème", "A", 28),
        ("4ème B", "4ème", "B", 28),
        ("3ème A", "3ème", "A", 28),
        ("3ème B", "3ème", "B", 28),
        
        # Lycée
        ("2nde A", "2nde", "Générale", 30),
        ("2nde B", "2nde", "Générale", 30),
        ("1ère S", "1ère", "Scientifique", 30),
        ("1ère ES", "1ère", "Économique et Social", 30),
        ("1ère L", "1ère", "Littéraire", 30),
        ("Terminale S", "Terminale", "Scientifique", 30),
        ("Terminale ES", "Terminale", "Économique et Social", 30),
        ("Terminale L", "Terminale", "Littéraire", 30),
    ]
    
    classes = []
    for name, level, section, max_students in classes_data:
        classe = Classe(
            name=name,
            level=level,
            section=section,
            academic_year="2024-2025",
            max_students=max_students,
            description=f"Classe de {name} pour l'année scolaire 2024-2025"
        )
        
        db.add(classe)
        classes.append(classe)
    
    db.commit()
    for classe in classes:
        db.refresh(classe)
    
    print(f"✅ {len(classes)} classes créées")
    return classes


def create_fake_subjects(db: Session, classes: list[Classe], teachers: list[Teacher]) -> list[Subject]:
    """Créer des matières fictives."""
    subjects_by_level = {
        "CP": ["Français", "Mathématiques", "Découverte du monde", "Arts plastiques", "EPS"],
        "CE1": ["Français", "Mathématiques", "Découverte du monde", "Arts plastiques", "EPS"],
        "CE2": ["Français", "Mathématiques", "Sciences", "Histoire-Géographie", "Arts plastiques", "EPS"],
        "CM1": ["Français", "Mathématiques", "Sciences", "Histoire-Géographie", "Arts plastiques", "EPS", "Anglais"],
        "CM2": ["Français", "Mathématiques", "Sciences", "Histoire-Géographie", "Arts plastiques", "EPS", "Anglais"],
        "6ème": ["Français", "Mathématiques", "Histoire-Géographie", "SVT", "Physique-Chimie", "Anglais", "Arts plastiques", "Musique", "EPS", "Technologie"],
        "5ème": ["Français", "Mathématiques", "Histoire-Géographie", "SVT", "Physique-Chimie", "Anglais", "Espagnol", "Arts plastiques", "Musique", "EPS", "Technologie"],
        "4ème": ["Français", "Mathématiques", "Histoire-Géographie", "SVT", "Physique-Chimie", "Anglais", "Espagnol", "Arts plastiques", "Musique", "EPS", "Technologie"],
        "3ème": ["Français", "Mathématiques", "Histoire-Géographie", "SVT", "Physique-Chimie", "Anglais", "Espagnol", "Arts plastiques", "Musique", "EPS", "Technologie"],
        "2nde": ["Français", "Mathématiques", "Histoire-Géographie", "SVT", "Physique-Chimie", "Anglais", "Espagnol", "EPS", "SES"],
        "1ère": ["Français", "Mathématiques", "Histoire-Géographie", "Philosophie", "Anglais", "Espagnol", "EPS"],
        "Terminale": ["Philosophie", "Mathématiques", "Histoire-Géographie", "Anglais", "Espagnol", "EPS"]
    }
    
    subjects = []
    subject_counter = 1
    
    for classe in classes:
        level = classe.level
        if level in subjects_by_level:
            for subject_name in subjects_by_level[level]:
                # Assigner un enseignant aléatoire
                teacher = random.choice(teachers)
                
                subject = Subject(
                    name=subject_name,
                    code=f"{subject_name[:3].upper()}{subject_counter:03d}",
                    description=f"{subject_name} pour la classe {classe.name}",
                    credits=random.randint(1, 4),
                    hours_per_week=random.randint(1, 6),
                    teacher_id=teacher.id,
                    classe_id=classe.id
                )
                
                db.add(subject)
                subjects.append(subject)
                subject_counter += 1
    
    db.commit()
    for subject in subjects:
        db.refresh(subject)
    
    print(f"✅ {len(subjects)} matières créées")
    return subjects


def create_fake_enrollments(db: Session, students: list[Student], classes: list[Classe]) -> list[Enrollment]:
    """Créer des inscriptions fictives."""
    enrollments = []
    
    # Répartir les étudiants dans les classes
    for student in students:
        # Choisir une classe aléatoire
        classe = random.choice(classes)
        
        enrollment = Enrollment(
            student_id=student.id,
            classe_id=classe.id,
            enrollment_date=fake.date_between(start_date='-1y', end_date='today'),
            status=random.choice(list(EnrollmentStatus))
        )
        
        db.add(enrollment)
        enrollments.append(enrollment)
    
    db.commit()
    for enrollment in enrollments:
        db.refresh(enrollment)
    
    print(f"✅ {len(enrollments)} inscriptions créées")
    return enrollments


def seed_database():
    """Fonction principale pour peupler la base de données."""
    print("🌱 Début du peuplement de la base de données...")
    
    # Créer une session
    db = SessionLocal()
    
    try:
        # 1. Créer l'administrateur
        admin = create_admin_user(db)
        
        # 2. Créer les utilisateurs
        teacher_users = create_fake_users(db, 15, UserRole.TEACHER)
        student_users = create_fake_users(db, 100, UserRole.STUDENT)
        parent_users = create_fake_users(db, 50, UserRole.PARENT)
        
        # 3. Créer les profils enseignants
        teachers = create_fake_teachers(db, teacher_users)
        
        # 4. Créer les profils étudiants
        students = create_fake_students(db, student_users)
        
        # 5. Créer les classes
        classes = create_fake_classes(db)
        
        # 6. Créer les matières
        subjects = create_fake_subjects(db, classes, teachers)
        
        # 7. Créer les inscriptions
        enrollments = create_fake_enrollments(db, students, classes)
        
        print("\n🎉 Peuplement terminé avec succès !")
        print(f"📊 Résumé:")
        print(f"   - 1 administrateur")
        print(f"   - {len(teacher_users)} enseignants")
        print(f"   - {len(student_users)} étudiants")
        print(f"   - {len(parent_users)} parents")
        print(f"   - {len(classes)} classes")
        print(f"   - {len(subjects)} matières")
        print(f"   - {len(enrollments)} inscriptions")
        
        print(f"\n🔑 Compte administrateur:")
        print(f"   Email: admin@ecole-prive.fr")
        print(f"   Mot de passe: admin123")
        
    except Exception as e:
        print(f"❌ Erreur lors du peuplement: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
