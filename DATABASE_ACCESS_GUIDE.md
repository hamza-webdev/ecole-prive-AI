# 🗄️ Guide d'accès aux données PostgreSQL

## 🔗 Liens d'accès rapide

### 1. **pgAdmin (Interface web recommandée)**
- **URL** : http://localhost:5050
- **Email** : admin@ecole-prive.fr
- **Mot de passe** : admin123

### 2. **Connexion directe PostgreSQL**
- **Host** : localhost
- **Port** : 5432
- **Database** : ecole_db
- **Username** : ecole_user
- **Password** : ecole_password

## 🚀 Démarrage rapide

### Démarrer pgAdmin
```bash
# Avec Docker Compose
docker-compose up -d pgadmin

# Ou avec le Makefile (si disponible)
make pgadmin
```

### Accéder aux données
1. Ouvrir http://localhost:5050 dans votre navigateur
2. Se connecter avec `admin@ecole-prive.fr` / `admin123`
3. Ajouter un serveur PostgreSQL avec les paramètres ci-dessus

## 📊 Structure de la base de données

### Tables principales

#### 👥 **users** - Utilisateurs du système
- `id` : Identifiant unique
- `email` : Adresse email (unique)
- `username` : Nom d'utilisateur (unique)
- `first_name`, `last_name` : Nom et prénom
- `role` : Rôle (admin, teacher, student, parent)
- `hashed_password` : Mot de passe haché
- `phone`, `address` : Coordonnées
- `is_active` : Statut actif/inactif
- `created_at`, `updated_at` : Timestamps

#### 🎓 **students** - Profils étudiants
- `id` : Identifiant unique
- `user_id` : Référence vers users
- `student_number` : Numéro étudiant (unique)
- `date_of_birth` : Date de naissance
- `parent_name`, `parent_phone`, `parent_email` : Contacts parents
- `emergency_contact` : Contact d'urgence
- `medical_info` : Informations médicales

#### 👨‍🏫 **teachers** - Profils enseignants
- `id` : Identifiant unique
- `user_id` : Référence vers users
- `employee_number` : Numéro employé (unique)
- `hire_date` : Date d'embauche
- `specialization` : Spécialisation
- `qualifications` : Qualifications
- `salary` : Salaire (en centimes)

#### 🏫 **classes** - Classes scolaires
- `id` : Identifiant unique
- `name` : Nom de la classe
- `level` : Niveau (CP, CE1, 6ème, etc.)
- `section` : Section (A, B, Scientifique, etc.)
- `academic_year` : Année scolaire
- `max_students` : Nombre maximum d'étudiants
- `description` : Description

#### 📚 **subjects** - Matières
- `id` : Identifiant unique
- `name` : Nom de la matière
- `code` : Code matière (unique)
- `description` : Description
- `credits` : Nombre de crédits
- `hours_per_week` : Heures par semaine
- `teacher_id` : Référence vers teachers
- `classe_id` : Référence vers classes

#### 📝 **enrollments** - Inscriptions
- `id` : Identifiant unique
- `student_id` : Référence vers students
- `classe_id` : Référence vers classes
- `enrollment_date` : Date d'inscription
- `status` : Statut (active, inactive, completed, dropped)

## 📈 Données générées avec Faker

### Statistiques actuelles
- **1 administrateur** : admin@ecole-prive.fr
- **15 enseignants** avec spécialisations variées
- **100 étudiants** avec informations complètes
- **50 parents** avec coordonnées
- **23 classes** (primaire, collège, lycée)
- **183 matières** assignées aux classes
- **100 inscriptions** d'étudiants

### Exemples de requêtes SQL

#### Lister tous les utilisateurs par rôle
```sql
SELECT role, COUNT(*) as count 
FROM users 
GROUP BY role 
ORDER BY count DESC;
```

#### Voir les étudiants avec leurs classes
```sql
SELECT 
    u.first_name, 
    u.last_name, 
    s.student_number,
    c.name as classe_name,
    c.level
FROM users u
JOIN students s ON u.id = s.user_id
JOIN enrollments e ON s.id = e.student_id
JOIN classes c ON e.classe_id = c.id
WHERE e.status = 'active'
ORDER BY c.level, u.last_name;
```

#### Matières par enseignant
```sql
SELECT 
    u.first_name || ' ' || u.last_name as teacher_name,
    t.specialization,
    COUNT(sub.id) as nb_subjects
FROM users u
JOIN teachers t ON u.id = t.user_id
LEFT JOIN subjects sub ON t.id = sub.teacher_id
GROUP BY u.id, u.first_name, u.last_name, t.specialization
ORDER BY nb_subjects DESC;
```

#### Classes avec nombre d'étudiants
```sql
SELECT 
    c.name,
    c.level,
    c.max_students,
    COUNT(e.id) as current_students
FROM classes c
LEFT JOIN enrollments e ON c.id = e.classe_id AND e.status = 'active'
GROUP BY c.id, c.name, c.level, c.max_students
ORDER BY c.level, c.name;
```

## 🛠️ Outils alternatifs

### 1. **Ligne de commande PostgreSQL**
```bash
# Accéder au shell PostgreSQL
docker-compose exec postgres psql -U ecole_user -d ecole_db

# Ou avec le Makefile
make db-shell
```

### 2. **DBeaver (Client lourd)**
- Télécharger : https://dbeaver.io/
- Configurer avec les paramètres de connexion ci-dessus

### 3. **TablePlus (macOS/Windows)**
- Télécharger : https://tableplus.com/
- Interface moderne et intuitive

### 4. **Adminer (Interface web légère)**
```bash
# Ajouter au docker-compose.yml si souhaité
adminer:
  image: adminer
  ports:
    - "8080:8080"
```

## 🔧 Configuration pgAdmin

### Première connexion
1. Ouvrir http://localhost:5050
2. Se connecter avec les identifiants
3. Clic droit sur "Servers" → "Register" → "Server"
4. **General tab** :
   - Name : École Privée DB
5. **Connection tab** :
   - Host : postgres (nom du service Docker)
   - Port : 5432
   - Database : ecole_db
   - Username : ecole_user
   - Password : ecole_password
6. Cliquer "Save"

### Navigation dans pgAdmin
- **Servers** → **École Privée DB** → **Databases** → **ecole_db** → **Schemas** → **public** → **Tables**
- Clic droit sur une table → "View/Edit Data" → "All Rows"
- Onglet "Query Tool" pour exécuter du SQL personnalisé

## 📱 Accès mobile

pgAdmin est responsive et fonctionne sur mobile/tablette via le navigateur web.

## 🔒 Sécurité

### En développement
- Mots de passe par défaut (à changer en production)
- Accès local uniquement

### En production
- Changer tous les mots de passe
- Configurer SSL/TLS
- Restreindre les accès réseau
- Utiliser des secrets Kubernetes

## 🆘 Dépannage

### pgAdmin ne démarre pas
```bash
# Vérifier les logs
docker-compose logs pgadmin

# Redémarrer le service
docker-compose restart pgadmin
```

### Impossible de se connecter à PostgreSQL
```bash
# Vérifier que PostgreSQL fonctionne
docker-compose ps postgres

# Tester la connexion
docker-compose exec postgres psql -U ecole_user -d ecole_db -c "SELECT version();"
```

### Données manquantes
```bash
# Repeupler la base de données
docker-compose exec backend python seed.py

# Ou réinitialiser complètement
docker-compose exec backend python reset_db.py
```

## 📚 Ressources utiles

- [Documentation pgAdmin](https://www.pgadmin.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQL Tutorial](https://www.w3schools.com/sql/)
- [FastAPI + PostgreSQL Guide](https://fastapi.tiangolo.com/tutorial/sql-databases/)
