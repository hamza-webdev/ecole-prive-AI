#!/usr/bin/env python3
"""
Script d'exécution pour le peuplement de la base de données
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.seed_data import seed_database

if __name__ == "__main__":
    print("🚀 Lancement du script de peuplement de données...")
    seed_database()
    print("✅ Script terminé !")
