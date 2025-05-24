# Documentation - École Privée AI

## 📋 Vue d'ensemble du projet

Application web complète pour la gestion d'une école privée développée avec :
- **Frontend** : Angular avec Angular Material
- **Backend** : FastAPI (Python)
- **Base de données** : PostgreSQL
- **Conteneurisation** : Docker + Docker Compose
- **Orchestration** : Kubernetes

## 🏗️ Architecture du projet

```
ecole-prive-AI/
├── frontend/           # Application Angular (à venir)
├── backend/            # API FastAPI
│   ├── app/
│   │   ├── models/     # Modèles SQLAlchemy
│   │   ├── schemas/    # Schémas Pydantic
│   │   ├── routers/    # Endpoints API
│   │   ├── config.py   # Configuration
│   │   ├── database.py # Configuration DB
│   │   ├── auth.py     # Authentification JWT
│   │   └── main.py     # Application principale
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── database/           # Scripts PostgreSQL
├── k8s/               # Manifests Kubernetes (à venir)
├── docker-compose.yml # Orchestration locale
└── README.md
```

## 🚀 Processus de développement réalisé

### Phase 1 : Initialisation du projet

1. **Création de la structure de base**
   ```bash
   mkdir ecole-prive-AI
   cd ecole-prive-AI
   ```

2. **Initialisation Git**
   ```bash
   git init
   git remote add origin https://github.com/hamza-webdev/ecole-prive-AI.git
   ```

3. **Création du README principal**
   - Description du projet
   - Architecture proposée
   - Fonctionnalités principales

### Phase 2 : Backend FastAPI

#### 2.1 Configuration de base

1. **Fichier requirements.txt**
   - FastAPI 0.104.1
   - Uvicorn avec support standard
   - SQLAlchemy 2.0.23
   - Alembic pour les migrations
   - psycopg2-binary pour PostgreSQL
   - python-jose pour JWT
   - passlib pour le hachage des mots de passe
   - Pydantic pour la validation

2. **Configuration (.env et config.py)**
   - Variables d'environnement
   - Configuration de la base de données
   - Paramètres de sécurité (JWT)
   - Configuration CORS

#### 2.2 Modèles de données

**Modèles créés :**

1. **User** (`models/user.py`)
   - Gestion des utilisateurs (admin, teacher, student, parent)
   - Authentification et autorisation
   - Informations personnelles

2. **Student** (`models/student.py`)
   - Profil étudiant
   - Informations académiques
   - Contacts d'urgence

3. **Teacher** (`models/teacher.py`)
   - Profil enseignant
   - Qualifications
   - Informations d'emploi

4. **Classe** (`models/classe.py`)
   - Gestion des classes
   - Niveaux et sections
   - Année académique

5. **Subject** (`models/subject.py`)
   - Matières enseignées
   - Crédits et heures
   - Association classe-professeur

6. **Enrollment** (`models/enrollment.py`)
   - Inscription des étudiants
   - Statut d'inscription
   - Historique

#### 2.3 Schémas Pydantic

**Schémas créés pour chaque modèle :**
- `*Create` : Création d'entités
- `*Update` : Mise à jour d'entités
- `*Response` : Réponses API

#### 2.4 Authentification et sécurité

1. **JWT Authentication** (`auth.py`)
   - Génération de tokens
   - Validation des tokens
   - Hachage des mots de passe avec bcrypt
   - Middleware d'authentification

2. **Endpoints d'authentification** (`routers/auth.py`)
   - POST `/auth/login` : Connexion utilisateur

#### 2.5 API Endpoints

**Routeurs créés :**

1. **Users** (`routers/users.py`)
   - POST `/users/` : Créer un utilisateur
   - GET `/users/` : Lister les utilisateurs
   - GET `/users/me` : Profil utilisateur connecté
   - GET `/users/{id}` : Utilisateur par ID
   - PUT `/users/{id}` : Mettre à jour
   - DELETE `/users/{id}` : Supprimer

2. **Students** (`routers/students.py`)
   - CRUD complet pour les étudiants

3. **Teachers** (`routers/teachers.py`)
   - CRUD complet pour les enseignants

4. **Classes** (`routers/classes.py`)
   - CRUD complet pour les classes

5. **Subjects** (`routers/subjects.py`)
   - CRUD complet pour les matières

### Phase 3 : Conteneurisation

#### 3.1 Docker Backend

1. **Dockerfile** (`backend/Dockerfile`)
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   RUN apt-get update && apt-get install -y gcc libpq-dev
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 8000
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
   ```

#### 3.2 Docker Compose

1. **Services configurés :**
   - **postgres** : Base de données PostgreSQL 15
   - **backend** : API FastAPI
   - **frontend** : Angular (préparé pour plus tard)

2. **Réseaux et volumes :**
   - Réseau `ecole_network`
   - Volume persistant `postgres_data`

### Phase 4 : Résolution des problèmes

#### 4.1 Problème CORS Configuration

**Problème identifié :**
```
pydantic_settings.sources.SettingsError: error parsing value for field "allowed_origins"
```

**Solution appliquée :**
1. Changement de `List[str]` vers `str` dans la configuration
2. Ajout d'une propriété `allowed_origins_list` pour parser manuellement
3. Mise à jour de la configuration CORS dans `main.py`

**Commit réalisé :**
```bash
git add .
git commit -m "Fix: Correction de la configuration CORS pour allowed_origins"
git push
```

## 🔧 Commandes utiles

### Développement local avec Docker

```bash
# Démarrer PostgreSQL
docker-compose up -d postgres

# Démarrer le backend
docker-compose up -d backend

# Voir les logs
docker-compose logs backend

# Redémarrer un service
docker-compose restart backend

# Arrêter tous les services
docker-compose down
```

### Tests API

```bash
# Test de base
curl http://localhost:8000

# Documentation Swagger
curl http://localhost:8000/docs

# Health check
curl http://localhost:8000/health
```

## 📊 Fonctionnalités implémentées

### ✅ Terminé
- [x] Structure du projet
- [x] Modèles de données complets
- [x] API REST avec FastAPI
- [x] Authentification JWT
- [x] Conteneurisation Docker
- [x] Configuration CORS
- [x] Documentation API automatique

### 🚧 En cours
- [ ] Résolution des imports de modèles
- [ ] Tests de l'API
- [ ] Frontend Angular

### 📋 À faire
- [ ] Interface utilisateur Angular
- [ ] Gestion des notes et évaluations
- [ ] Système de présences
- [ ] Notifications et messages
- [ ] Rapports et statistiques
- [ ] Déploiement Kubernetes
- [ ] Tests unitaires et d'intégration

## 🐛 Problèmes rencontrés et solutions

### 1. Configuration CORS avec Pydantic
- **Problème** : Erreur de parsing JSON pour `allowed_origins`
- **Solution** : Utilisation d'une chaîne avec parsing manuel
- **Commit** : `30e6b75`

### 2. Import des modèles SQLAlchemy
- **Problème** : `ImportError: cannot import name 'Base'`
- **Solution** : Import direct depuis `database.py`
- **Statut** : En cours de résolution

## 📝 Prochaines étapes

1. **Finaliser le backend**
   - Corriger les imports de modèles
   - Tester tous les endpoints
   - Ajouter la validation des données

2. **Développer le frontend Angular**
   - Initialiser le projet Angular
   - Créer les composants de base
   - Implémenter l'authentification

3. **Intégration et tests**
   - Tests end-to-end
   - Validation de l'intégration frontend-backend

4. **Déploiement**
   - Configuration Kubernetes
   - CI/CD avec GitHub Actions
   - Déploiement en production

## 🔗 Liens utiles

- **Repository** : https://github.com/hamza-webdev/ecole-prive-AI
- **API Documentation** : http://localhost:8000/docs
- **Base de données** : PostgreSQL sur port 5432
- **Backend API** : http://localhost:8000
