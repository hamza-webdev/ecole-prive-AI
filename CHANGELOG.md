# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Non publié]

### En cours
- Résolution des imports de modèles SQLAlchemy
- Tests des endpoints API
- Développement du frontend Angular

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
