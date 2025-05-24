# Guide de développement - École Privée AI

## 🚀 Démarrage rapide

### Prérequis
- Docker et Docker Compose
- Git
- Python 3.11+ (pour le développement local)
- Node.js 18+ (pour le frontend Angular)

### Installation

1. **Cloner le repository**
   ```bash
   git clone https://github.com/hamza-webdev/ecole-prive-AI.git
   cd ecole-prive-AI
   ```

2. **Démarrer l'environnement de développement**
   ```bash
   # Démarrer PostgreSQL
   docker-compose up -d postgres
   
   # Démarrer le backend
   docker-compose up -d backend
   ```

3. **Vérifier que tout fonctionne**
   ```bash
   # Test de l'API
   curl http://localhost:8000
   
   # Documentation Swagger
   open http://localhost:8000/docs
   ```

## 🏗️ Architecture de développement

### Structure des branches
```
main                 # Production
├── develop         # Développement principal
├── feature/*       # Nouvelles fonctionnalités
├── bugfix/*        # Corrections de bugs
└── hotfix/*        # Corrections urgentes
```

### Workflow de développement

1. **Créer une branche feature**
   ```bash
   git checkout -b feature/nom-de-la-fonctionnalite
   ```

2. **Développer et tester**
   ```bash
   # Faire les modifications
   # Tester localement
   docker-compose restart backend
   ```

3. **Commit avec convention**
   ```bash
   git add .
   git commit -m "feat: description de la fonctionnalité"
   ```

4. **Push et Pull Request**
   ```bash
   git push origin feature/nom-de-la-fonctionnalite
   # Créer une PR sur GitHub
   ```

## 🔧 Développement Backend

### Structure du code
```
backend/app/
├── models/         # Modèles SQLAlchemy
├── schemas/        # Schémas Pydantic
├── routers/        # Endpoints API
├── services/       # Logique métier (à créer)
├── utils/          # Utilitaires (à créer)
├── tests/          # Tests (à créer)
├── config.py       # Configuration
├── database.py     # Configuration DB
├── auth.py         # Authentification
└── main.py         # Application principale
```

### Ajouter un nouveau modèle

1. **Créer le modèle SQLAlchemy**
   ```python
   # backend/app/models/nouveau_modele.py
   from sqlalchemy import Column, Integer, String
   from ..database import Base
   
   class NouveauModele(Base):
       __tablename__ = "nouveau_modeles"
       
       id = Column(Integer, primary_key=True, index=True)
       nom = Column(String, nullable=False)
   ```

2. **Créer les schémas Pydantic**
   ```python
   # backend/app/schemas/nouveau_modele.py
   from pydantic import BaseModel
   
   class NouveauModeleCreate(BaseModel):
       nom: str
   
   class NouveauModeleResponse(BaseModel):
       id: int
       nom: str
       
       class Config:
           from_attributes = True
   ```

3. **Créer le routeur**
   ```python
   # backend/app/routers/nouveau_modele.py
   from fastapi import APIRouter, Depends
   from ..models.nouveau_modele import NouveauModele
   from ..schemas.nouveau_modele import NouveauModeleCreate, NouveauModeleResponse
   
   router = APIRouter()
   
   @router.post("/", response_model=NouveauModeleResponse)
   def create_nouveau_modele(modele: NouveauModeleCreate):
       # Logique de création
       pass
   ```

4. **Ajouter au main.py**
   ```python
   from .routers import nouveau_modele
   app.include_router(nouveau_modele.router, prefix="/nouveau-modeles", tags=["Nouveau Modeles"])
   ```

### Tests

1. **Structure des tests**
   ```
   backend/tests/
   ├── conftest.py         # Configuration pytest
   ├── test_auth.py        # Tests authentification
   ├── test_users.py       # Tests utilisateurs
   └── test_models.py      # Tests modèles
   ```

2. **Exemple de test**
   ```python
   # backend/tests/test_users.py
   import pytest
   from fastapi.testclient import TestClient
   from app.main import app
   
   client = TestClient(app)
   
   def test_create_user():
       response = client.post("/users/", json={
           "email": "test@example.com",
           "username": "testuser",
           "password": "testpass"
       })
       assert response.status_code == 201
   ```

3. **Lancer les tests**
   ```bash
   cd backend
   pytest
   ```

## 🎨 Développement Frontend (Angular)

### Structure prévue
```
frontend/
├── src/
│   ├── app/
│   │   ├── components/     # Composants réutilisables
│   │   ├── pages/          # Pages de l'application
│   │   ├── services/       # Services Angular
│   │   ├── models/         # Interfaces TypeScript
│   │   ├── guards/         # Guards de route
│   │   └── interceptors/   # Intercepteurs HTTP
│   ├── assets/             # Ressources statiques
│   └── environments/       # Configuration environnements
├── angular.json
├── package.json
└── Dockerfile
```

### Initialisation (à faire)
```bash
cd frontend
ng new ecole-frontend --routing --style=scss
ng add @angular/material
```

## 🐛 Debugging et résolution de problèmes

### Logs Docker
```bash
# Voir les logs en temps réel
docker-compose logs -f backend

# Logs PostgreSQL
docker-compose logs postgres

# Entrer dans le conteneur
docker-compose exec backend bash
```

### Debugging Python
```python
# Ajouter des points d'arrêt
import pdb; pdb.set_trace()

# Ou utiliser des logs
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Message de debug")
```

### Problèmes courants

1. **Erreur de connexion à la base de données**
   ```bash
   # Vérifier que PostgreSQL est démarré
   docker-compose ps
   
   # Redémarrer si nécessaire
   docker-compose restart postgres
   ```

2. **Erreur d'import Python**
   ```bash
   # Reconstruire l'image
   docker-compose build backend
   docker-compose up -d backend
   ```

3. **Problème de CORS**
   ```python
   # Vérifier la configuration dans config.py
   allowed_origins: str = "http://localhost:4200,http://localhost:3000"
   ```

## 📝 Conventions de code

### Python (Backend)
- **PEP 8** pour le style
- **Type hints** obligatoires
- **Docstrings** pour les fonctions publiques
- **Black** pour le formatage automatique

```python
def create_user(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """
    Créer un nouvel utilisateur.
    
    Args:
        user_data: Données de l'utilisateur à créer
        db: Session de base de données
        
    Returns:
        UserResponse: Utilisateur créé
        
    Raises:
        HTTPException: Si l'email existe déjà
    """
    pass
```

### TypeScript (Frontend)
- **Angular Style Guide** officiel
- **Interfaces** pour les types
- **Services** pour la logique métier
- **Components** pour l'UI

### Git
- **Commits atomiques** (une fonctionnalité = un commit)
- **Messages descriptifs** en français
- **Branches nommées** selon la convention

## 🔄 Processus de release

### Versioning
- **Semantic Versioning** (MAJOR.MINOR.PATCH)
- **Tags Git** pour les releases
- **CHANGELOG.md** mis à jour

### Étapes de release
1. **Finaliser les fonctionnalités**
2. **Tests complets**
3. **Mise à jour de la documentation**
4. **Création du tag**
   ```bash
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```

## 🚀 Déploiement

### Environnements
- **Development** : Local avec Docker
- **Staging** : Kubernetes (à configurer)
- **Production** : Kubernetes (à configurer)

### Variables d'environnement
```bash
# Development
DATABASE_URL=postgresql://ecole_user:ecole_password@localhost:5432/ecole_db

# Production
DATABASE_URL=postgresql://user:pass@prod-db:5432/ecole_prod
SECRET_KEY=super-secret-production-key
```

## 📚 Ressources

### Documentation
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Angular](https://angular.io/docs)
- [Docker](https://docs.docker.com/)

### Outils recommandés
- **IDE** : VS Code avec extensions Python et Angular
- **API Testing** : Postman ou Insomnia
- **Database** : pgAdmin ou DBeaver
- **Git GUI** : GitKraken ou SourceTree
