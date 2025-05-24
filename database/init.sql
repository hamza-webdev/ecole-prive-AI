-- Script d'initialisation de la base de données
-- Ce script sera exécuté automatiquement lors de la création du conteneur PostgreSQL

-- Créer des extensions utiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Créer des index pour améliorer les performances
-- (Les tables seront créées automatiquement par SQLAlchemy)

-- Insérer des données de test (optionnel)
-- Ces données seront ajoutées après la création des tables par l'application
