# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Non publié]

### En cours
- Développement du frontend Angular
- Tests unitaires et d'intégration
- Configuration Kubernetes pour le déploiement

## [0.2.0] - 2024-01-XX

### Ajouté
- **Système de génération de données fictives** avec Faker
  - Script `seed_data.py` pour créer des données réalistes
  - Génération automatique de 15 enseignants, 100 étudiants, 50 parents
  - Création de 23 classes (primaire, collège, lycée)
  - 183 matières avec attribution aux classes et enseignants
  - 100 inscriptions d'étudiants dans les classes
  - Compte administrateur par défaut (admin@ecole-prive.fr / admin123)
- **Scripts utilitaires** pour la gestion de la base de données
  - `clear_data.py` : Vider la base de données
  - `reset_db.py` : Réinitialiser complètement (vider + repeupler)
  - `seed.py` : Script d'exécution du peuplement
- **Makefile** avec commandes simplifiées
  - `make seed` : Peupler avec des données fictives
  - `make clear` : Vider la base de données
  - `make reset` : Réinitialiser complètement
  - `make install` : Installation complète (build + up + seed)
  - Commandes Docker et développement
- **Données en français** générées avec Faker locale française

### Technique
- Faker 20.1.0 pour la génération de données
- Scripts Python pour la gestion de la base
- Makefile pour l'automatisation des tâches

## [0.1.0] - 2024-01-XX

### Ajouté
- Structure initiale du projet
- Backend FastAPI complet avec :
  - Modèles SQLAlchemy (User, Student, Teacher, Classe, Subject, Enrollment)
  - Schémas Pydantic pour validation
  - Authentification JWT
  - API REST complète (CRUD pour toutes les entités)
  - Configuration avec variables d'environnement
- Conteneurisation Docker :
  - Dockerfile pour le backend
  - Docker Compose avec PostgreSQL et backend
  - Configuration des réseaux et volumes
- Documentation :
  - README principal
  - Documentation technique complète
  - Swagger UI automatique

### Corrigé
- **[30e6b75]** Configuration CORS pour `allowed_origins`
  - Problème : Erreur de parsing JSON avec pydantic_settings
  - Solution : Changement de `List[str]` vers `str` avec parsing manuel
  - Ajout de la propriété `allowed_origins_list`

### Technique
- Python 3.11
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- PostgreSQL 15
- Docker & Docker Compose

## Commits détaillés

### [2e44a7e] - feat: Ajout du système de génération de données fictives avec Faker
```
- Ajout de faker==20.1.0 aux dépendances
- Script seed_data.py pour générer des données réalistes
- Création automatique d'un admin (admin@ecole-prive.fr / admin123)
- Génération de 15 enseignants, 100 étudiants, 50 parents
- Création de 23 classes (primaire, collège, lycée)
- Génération de 183 matières avec attribution aux classes
- 100 inscriptions d'étudiants dans les classes
- Scripts utilitaires : clear_data.py, reset_db.py
- Makefile avec commandes pour seed, clear, reset
- Tests réussis : API fonctionnelle et authentification OK
```

**Fichiers ajoutés :**
- `backend/requirements.txt` : Ajout de faker==20.1.0
- `backend/app/seed_data.py` : Script principal de génération
- `backend/app/clear_data.py` : Script de nettoyage
- `backend/reset_db.py` : Script de réinitialisation
- `backend/seed.py` : Script d'exécution
- `Makefile` : Commandes automatisées

**Impact :** Base de données peuplée avec des données réalistes pour le développement et les tests

### [30e6b75] - Fix: Correction de la configuration CORS pour allowed_origins
```
- Changement de List[str] vers str avec parsing manuel
- Ajout de la propriété allowed_origins_list pour la compatibilité
- Correction de l'erreur JSON parsing dans pydantic_settings
```

**Fichiers modifiés :**
- `backend/app/config.py` : Modification du type `allowed_origins`
- `backend/app/main.py` : Utilisation de `allowed_origins_list`
- `backend/.env` : Ajout du fichier de configuration

**Impact :** Résolution de l'erreur de démarrage du serveur FastAPI

### [64167ad] - Initial commit
```
- Création de la structure du projet
- Implémentation complète du backend FastAPI
- Configuration Docker et Docker Compose
- Documentation initiale
```

**Fichiers ajoutés :**
- Structure complète du backend
- Modèles et schémas
- Routeurs API
- Configuration Docker
- Documentation

## Processus de développement

### Workflow Git
1. **Développement** : Travail sur une fonctionnalité
2. **Test** : Validation locale avec Docker
3. **Commit** : Message descriptif avec contexte
4. **Push** : Envoi vers le repository distant

### Convention de commits
```
<type>: <description courte>

<description détaillée>
- Point 1
- Point 2
```

**Types utilisés :**
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage, pas de changement de code
- `refactor:` Refactoring de code
- `test:` Ajout ou modification de tests
- `chore:` Maintenance, configuration

### Processus de résolution de bugs

1. **Identification** : Analyse des logs et erreurs
2. **Diagnostic** : Compréhension de la cause racine
3. **Solution** : Implémentation du correctif
4. **Test** : Validation de la correction
5. **Commit** : Documentation de la correction
6. **Push** : Partage de la solution

### Exemple de résolution (CORS)

1. **Erreur identifiée :**
   ```
   pydantic_settings.sources.SettingsError: error parsing value for field "allowed_origins"
   ```

2. **Diagnostic :**
   - Pydantic essaie de parser la chaîne comme du JSON
   - La configuration `List[str]` ne fonctionne pas avec les variables d'environnement

3. **Solution :**
   - Changement vers `str` avec parsing manuel
   - Propriété calculée pour la compatibilité

4. **Test :**
   ```bash
   docker-compose restart backend
   curl http://localhost:8000
   ```

5. **Commit et push :**
   ```bash
   git add .
   git commit -m "Fix: Correction de la configuration CORS"
   git push
   ```

## Métriques du projet

### Lignes de code
- Backend Python : ~1500 lignes
- Configuration Docker : ~50 lignes
- Documentation : ~300 lignes

### Fichiers créés
- Modèles : 6 fichiers
- Schémas : 5 fichiers
- Routeurs : 5 fichiers
- Configuration : 4 fichiers
- Docker : 2 fichiers

### Fonctionnalités
- Endpoints API : 25+
- Modèles de données : 6
- Authentification : JWT complète
- Documentation : Swagger automatique
