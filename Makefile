# Makefile pour l'application École Privée AI

.PHONY: help build up down logs restart seed clear reset test

# Variables
DOCKER_COMPOSE = docker-compose
BACKEND_CONTAINER = ecole_backend

help: ## Afficher l'aide
	@echo "Commandes disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Construire les images Docker
	$(DOCKER_COMPOSE) build

up: ## Démarrer tous les services
	$(DOCKER_COMPOSE) up -d

down: ## Arrêter tous les services
	$(DOCKER_COMPOSE) down

logs: ## Voir les logs du backend
	$(DOCKER_COMPOSE) logs -f backend

logs-all: ## Voir les logs de tous les services
	$(DOCKER_COMPOSE) logs -f

restart: ## Redémarrer le backend
	$(DOCKER_COMPOSE) restart backend

restart-all: ## Redémarrer tous les services
	$(DOCKER_COMPOSE) restart

# Base de données
seed: ## Peupler la base avec des données fictives
	$(DOCKER_COMPOSE) exec backend python seed.py

clear: ## Vider la base de données
	$(DOCKER_COMPOSE) exec backend python -c "from app.clear_data import clear_database; clear_database()"

reset: ## Réinitialiser complètement la base (vider + repeupler)
	$(DOCKER_COMPOSE) exec backend python reset_db.py

# Développement
shell: ## Accéder au shell du conteneur backend
	$(DOCKER_COMPOSE) exec backend bash

db-shell: ## Accéder au shell PostgreSQL
	$(DOCKER_COMPOSE) exec postgres psql -U ecole_user -d ecole_db

# Tests
test: ## Lancer les tests (à implémenter)
	$(DOCKER_COMPOSE) exec backend pytest

# API
api-docs: ## Ouvrir la documentation API
	@echo "Documentation API disponible sur: http://localhost:8000/docs"

api-test: ## Tester l'API
	curl -s http://localhost:8000 | jq .

# Nettoyage
clean: ## Nettoyer les conteneurs et volumes
	$(DOCKER_COMPOSE) down -v
	docker system prune -f

# Installation
install: build up seed ## Installation complète (build + up + seed)
	@echo ""
	@echo "🎉 Installation terminée !"
	@echo "📚 Documentation API: http://localhost:8000/docs"
	@echo "🔑 Admin: admin@ecole-prive.fr / admin123"

# Statut
status: ## Afficher le statut des services
	$(DOCKER_COMPOSE) ps
