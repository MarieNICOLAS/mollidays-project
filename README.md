
# 🌍 Mollidays – Plateforme de Réservation de Voyages Parent-Enfant

Bienvenue dans le dépôt du projet **Mollidays**, une application web full-stack permettant à des duos parent-enfant adulte de réserver des circuits de voyage immersifs.  
Le projet est conçu dans le cadre du titre professionnel **Concepteur Développeur d'Applications – RNCP 37873**.

---

## 🛠 Stack technique

| Côté            | Technologie             |
|-----------------|-------------------------|
| Frontend        | React.js (Next.js)      |
| Backend         | Django REST Framework   |
| Base de données | PostgreSQL + MongoDB    |
| Authentification| JWT (via SimpleJWT)     |
| CI/CD           | GitHub Actions          |
| Conteneurisation| Docker + Docker Compose |
| Tests           | Django TestCase         |

---

## 🚀 Lancer le projet en local (avec Docker)

### 1. Cloner le projet

```bash
git clone https://github.com/ton-profil/mollidays-project.git
cd mollidays-project
```

### 2. Créer un fichier `.env.docker`

```env
# Exemple pour le backend
POSTGRES_DB=mollidays
POSTGRES_USER=mollidays_user
POSTGRES_PASSWORD=securepassword
SECRET_KEY=changeme
DEBUG=True
```

### 3. Lancer les conteneurs Docker

```bash
docker-compose build
docker-compose up -d
```

- Le backend sera disponible sur [http://localhost:8000/api/](http://localhost:8000/api/)
- Le frontend sur [http://localhost:3000](http://localhost:3000)

### 4. Appliquer les migrations Django

```bash
docker-compose exec backend python manage.py migrate
```

Créer un super utilisateur :

```bash
docker-compose exec backend python manage.py createsuperuser
```

---

## 📂 Structure du projet

```bash
mollidays-project/
├── backend/                  # Django + DRF
│   ├── users/
│   ├── circuits/
│   ├── bookings/
│   └── ...
├── frontend/                 # Next.js (React)
│   ├── pages/
│   ├── components/
│   └── ...
├── docker-compose.yml
├── .env.docker
└── README.md
```

---

## ✅ Tests

Pour lancer les tests backend :

```bash
docker-compose exec backend python manage.py test
```

---

## ⚙️ Intégration Continue (CI/CD)

Chaque `push` déclenche automatiquement :
- Les tests Django
- Le linting de base

Fichier de workflow : `.github/workflows/backend.yml`

---

## 🧪 Exemple de requêtes (via Insomnia/Postman)

- `POST /api/register/` – Inscription
- `POST /api/token/` – Connexion (JWT)
- `GET /api/circuits/` – Liste des circuits
- `POST /api/bookings/` – Réserver un circuit

---

## 🗂 Base de données

- **SQL (PostgreSQL)** : utilisateurs, circuits, réservations, paiements.
- **NoSQL (MongoDB)** : avis utilisateurs.

---

## 🛡 Sécurité

- Authentification via JWT
- Chiffrement des mots de passe avec `pbkdf2_sha256`
- Protection contre XSS, CSRF, Injection SQL
- Variables sensibles stockées dans `.env`

---

## 🧭 Roadmap

- [x] Authentification sécurisée
- [x] Visualisation des circuits
- [x] Réservations de voyages
- [x] Système de paiement
- [ ] Notifications email
- [ ] Application mobile (v2)

---

## 👩‍💻 Auteure

Marie NICOLAS – [LinkedIn](https://www.linkedin.com/in/...)  
Projet soutenu dans le cadre du titre **CDA – RNCP 37873** à Ensitech.

---

## 📜 Licence

Projet pédagogique – non destiné à la mise en production commerciale immédiate.
