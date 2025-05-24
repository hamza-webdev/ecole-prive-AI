#!/usr/bin/env python3
"""
Script pour réinitialiser complètement la base de données
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.clear_data import clear_database
from app.seed_data import seed_database

if __name__ == "__main__":
    print("🔄 Réinitialisation complète de la base de données...")
    
    # 1. Vider la base
    clear_database()
    
    print("\n" + "="*50)
    
    # 2. Repeupler avec des données fictives
    seed_database()
    
    print("\n🎉 Réinitialisation terminée !")
