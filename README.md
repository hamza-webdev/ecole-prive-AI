# École Privée - Système de Gestion

Application web complète pour la gestion d'une école privée.

## Architecture

- **Frontend**: Angular avec Angular Material
- **Backend**: FastAPI (Python)
- **Base de données**: PostgreSQL
- **Conteneurisation**: Docker + Docker Compose
- **Orchestration**: Kubernetes

## Structure du projet

```
ecole-prive-AI/
├── frontend/           # Application Angular
├── backend/            # API FastAPI
├── database/           # Scripts et migrations PostgreSQL
├── docker/             # Dockerfiles et configurations
├── k8s/               # Manifests Kubernetes
├── docker-compose.yml # Orchestration locale
└── README.md          # Documentation
```

## Fonctionnalités

- 👥 Gestion des utilisateurs (étudiants, professeurs, administrateurs)
- 📚 Gestion des classes et matières
- 📅 Planning et emploi du temps
- 📊 Notes et évaluations
- ✅ Présences/absences
- 💬 Communication (messages, notifications)
- 💰 Facturation et paiements
- 📈 Rapports et statistiques

## Démarrage rapide

### Développement local
```bash
# Démarrer tous les services
docker-compose up -d

# Frontend: http://localhost:4200
# Backend API: http://localhost:8000
# Base de données: localhost:5432
```

### Production avec Kubernetes
```bash
kubectl apply -f k8s/
```

## Documentation

- [API Documentation](http://localhost:8000/docs) - Swagger UI
- [Frontend Documentation](./frontend/README.md)
- [Backend Documentation](./backend/README.md)
