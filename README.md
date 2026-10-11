<div align="center">

# 📧 EneoNewsletter

### Plateforme professionnelle de gestion de newsletters et notifications

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![Celery](https://img.shields.io/badge/Celery-5.5-brightgreen.svg)](https://docs.celeryproject.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📋 Table des matières

- [À propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Technologies](#-technologies)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Commandes disponibles](#-commandes-disponibles)
- [Déploiement](#-déploiement)
- [Tests](#-tests)
- [Contribution](#-contribution)
- [Licence](#-licence)
- [Auteur](#-auteur)

---

## 📖 À propos

**EneoNewsletter** est une application web professionnelle développée avec Django pour la gestion complète de newsletters et la notification automatique des coupures d'électricité programmées. Conçue spécifiquement pour Eneo, cette plateforme offre une solution robuste et scalable pour la communication avec les abonnés.

### Points forts

- ✅ **Architecture moderne** : Stack technologique éprouvée (Django, Celery, Redis)
- ✅ **Haute disponibilité** : Traitement asynchrone des tâches avec Celery Beat
- ✅ **Scalabilité** : Conteneurisation complète avec Docker
- ✅ **Production-ready** : Configuration optimisée pour le déploiement sur Render
- ✅ **Interface intuitive** : Interface d'administration Django personnalisée

---

## ✨ Fonctionnalités

### Gestion des newsletters

- 📝 **Création et édition** de newsletters avec éditeur riche
- 📊 **Tableau de bord** avec statistiques d'envoi et engagement
- 👥 **Gestion des abonnés** avec import/export CSV
- 📅 **Programmation d'envois** avec planification flexible
- 📧 **Templates personnalisables** avec design responsive
- 🔍 **Suivi détaillé** des ouvertures et clics

### Notifications de coupures

- ⚡ **Récupération automatique** des coupures programmées via API Eneo
- 🎯 **Ciblage intelligent** des abonnés par quartier
- 📬 **Notifications par email** automatiques et personnalisées
- 🗺️ **Gestion géographique** (région, ville, quartier)
- 📝 **Historique complet** des notifications envoyées

### Administration

- 🔐 **Interface d'administration** Django sécurisée
- 👤 **Gestion des utilisateurs** et permissions
- 📈 **Statistiques en temps réel** sur les envois
- 🔔 **Logs détaillés** des activités système
- ⚙️ **Configuration flexible** via variables d'environnement

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Client    │────▶│  Django Web  │────▶│ PostgreSQL  │
│  (Browser)  │     │   (Gunicorn) │     │  Database   │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐     ┌─────────────┐
                    │    Redis     │◀────│   Celery    │
                    │   (Cache &   │     │   Worker    │
                    │    Broker)   │     └─────────────┘
                    └──────────────┘            │
                           │                     │
                           ▼                     ▼
                    ┌──────────────┐     ┌─────────────┐
                    │ Celery Beat  │     │    SMTP     │
                    │  (Scheduler) │     │   Server    │
                    └──────────────┘     └─────────────┘
```

### Flux de travail

1. **Requêtes HTTP** : Gérées par Gunicorn et Django
2. **Tâches asynchrones** : Déléguées à Celery via Redis
3. **Planification** : Celery Beat déclenche les tâches périodiques
4. **Stockage** : PostgreSQL pour les données persistantes
5. **Cache** : Redis pour les performances optimales
6. **Emails** : Envoi via SMTP configuré

---

## 🛠️ Technologies

| Catégorie | Technologies |
|-----------|--------------|
| **Backend** | Python 3.11, Django 5.2 |
| **Task Queue** | Celery 5.5, Redis 7 |
| **Base de données** | PostgreSQL 17 |
| **Cache** | Redis |
| **Serveur web** | Gunicorn, WhiteNoise |
| **Conteneurisation** | Docker, Docker Compose |
| **Déploiement** | Render (PaaS) |
| **Email** | SMTP, Templates HTML |

---

## 📦 Prérequis

### Pour le développement local

- **Docker** ≥ 20.10 et **Docker Compose** ≥ 2.0
- **Python** ≥ 3.11 (pour développement hors Docker)
- **Git** pour le contrôle de version

### Pour le déploiement en production

- Compte **Render** ou autre plateforme cloud
- Service **PostgreSQL** (géré ou auto-hébergé)
- Service **Redis** (géré ou auto-hébergé)
- Serveur **SMTP** (Gmail, SendGrid, Mailgun, etc.)

---

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/Starland9/EneoNewsletter.git
cd EneoNewsletter
```

### 2. Créer le fichier de configuration

Créez un fichier `.env` à la racine du projet :

```bash
cp .env.example .env  # Si disponible, sinon créez le fichier manuellement
```

Voir la section [Configuration](#-configuration) pour les détails des variables.

### 3. Lancer avec Docker Compose

```bash
# Construire et démarrer tous les services
docker-compose up --build -d

# Vérifier le statut des conteneurs
docker-compose ps
```

### 4. Initialiser la base de données

```bash
# Appliquer les migrations
docker-compose exec web python manage.py migrate

# Créer un superutilisateur
docker-compose exec web python manage.py createsuperuser

# Collecter les fichiers statiques (pour production)
docker-compose exec web python manage.py collectstatic --noinput
```

### 5. Accéder à l'application

- **Application web** : http://localhost:10000
- **Interface admin** : http://localhost:10000/admin
- **Newsletter** : http://localhost:10000/newsletter/

---

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```bash
# Django
SECRET_KEY=votre_secret_key_super_securisee
DEBUG=0  # 1 uniquement en développement
ALLOWED_HOSTS=localhost,127.0.0.1,votre-domaine.com
DJANGO_SETTINGS_MODULE=EneoNewsletter.settings
DOMAIN=votre-domaine.com

# Base de données PostgreSQL (externe : URL du service Dokploy ou autre)
# Format : postgresql://user:password@host:5432/dbname
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis (externe : URL du service Dokploy ou autre ; rediss:// pour TLS)
# Celery réutilise REDIS_URL (voir settings.py)
REDIS_URL=redis://host:6379/0

# Configuration Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com  # Ou autre serveur SMTP
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre.email@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_application
DEFAULT_FROM_EMAIL=noreply@eneo.cm

# Localisation
TIME_ZONE=Africa/Douala
LANGUAGE_CODE=fr-fr

# Gunicorn (Production)
WEB_CONCURRENCY=4

# Celery : utilise REDIS_URL (voir settings.py)
```

### Configuration SMTP recommandée

#### Gmail (avec mot de passe d'application)
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

#### SendGrid
```bash
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=votre_api_key_sendgrid
```

#### Mailgun
```bash
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

---

## 💻 Utilisation

### Gestion des newsletters

1. **Connexion à l'admin** : http://localhost:10000/admin
2. **Créer une newsletter** : Section "Newsletters" → "Ajouter"
3. **Gérer les abonnés** : Section "Subscribers" → Import CSV disponible
4. **Programmer un envoi** : Définir date et heure d'envoi
5. **Consulter les statistiques** : Tableau de bord admin

### Gestion des coupures

1. **Récupération automatique** : Tâche Celery périodique (API Eneo)
2. **Notification automatique** : Envoi aux abonnés concernés par quartier
3. **Consultation** : Interface admin → Section "Coupures programmées"

### Consultation publique

Les newsletters envoyées sont accessibles publiquement :
- Liste : http://localhost:10000/newsletter/
- Détail : http://localhost:10000/newsletter/{id}/

---

## 📁 Structure du projet

```
EneoNewsletter/
│
├── EneoNewsletter/          # Configuration principale Django
│   ├── __init__.py
│   ├── settings.py          # Paramètres Django
│   ├── urls.py              # Routes principales
│   ├── wsgi.py              # Point d'entrée WSGI
│   └── celery.py            # Configuration Celery
│
├── newsletter/              # Application de gestion des newsletters
│   ├── models.py            # Modèles (Newsletter, Subscriber)
│   ├── admin.py             # Interface d'administration
│   ├── tasks.py             # Tâches Celery (envoi emails)
│   ├── views.py             # Vues publiques
│   ├── forms.py             # Formulaires
│   ├── urls.py              # Routes de l'app
│   └── templates/           # Templates HTML
│       └── newsletter/
│           ├── base.html
│           ├── list.html
│           └── detail.html
│
├── coupure/                 # Application de gestion des coupures
│   ├── models.py            # Modèle Coupure
│   ├── admin.py             # Interface admin coupures
│   ├── tasks.py             # Tâches de récupération et notification
│   ├── signals.py           # Signaux Django
│   ├── management/
│   │   └── commands/
│   │       └── fetch_coupures.py  # Commande manuelle
│   └── templates/
│       └── coupure/
│           └── emails/
│               └── coupure_notification.html
│
├── docker-compose.yml       # Configuration Docker Compose
├── Dockerfile               # Image Docker de l'application
├── requirements.txt         # Dépendances Python
├── manage.py                # Script de gestion Django
├── render.yaml              # Configuration déploiement Render
├── build.sh                 # Script de build
├── create_superuser.py      # Script création admin
└── README.md                # Ce fichier
```

---

## 🎯 Commandes disponibles

### Gestion Django

```bash
# Créer les migrations
docker-compose exec web python manage.py makemigrations

# Appliquer les migrations
docker-compose exec web python manage.py migrate

# Créer un superutilisateur
docker-compose exec web python manage.py createsuperuser

# Collecter les fichiers statiques
docker-compose exec web python manage.py collectstatic

# Lancer le shell Django
docker-compose exec web python manage.py shell
```

### Gestion des coupures

```bash
# Récupérer manuellement les coupures depuis l'API Eneo
docker-compose exec web python manage.py fetch_coupures
```

### Celery

```bash
# Voir les tâches actives
docker-compose exec celery celery -A EneoNewsletter inspect active

# Voir les tâches planifiées
docker-compose exec celery-beat celery -A EneoNewsletter inspect scheduled

# Purger la queue
docker-compose exec celery celery -A EneoNewsletter purge
```

### Docker

```bash
# Voir les logs en temps réel
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f web
docker-compose logs -f celery

# Redémarrer un service
docker-compose restart web

# Arrêter tous les services
docker-compose down

# Supprimer également les volumes
docker-compose down -v
```

---

## 🌐 Déploiement

### Déploiement sur Render

Le projet est configuré pour un déploiement simple sur Render via le fichier `render.yaml`.

#### 1. Prérequis Render

- Compte Render : https://render.com
- Repository GitHub connecté

#### 2. Configuration

1. **Fork/Push** le projet sur votre GitHub
2. **Créer un nouveau Blueprint** sur Render
3. **Connecter** votre repository
4. Render détectera automatiquement `render.yaml`

#### 3. Services déployés

Le blueprint configure automatiquement :
- ✅ Service Web (Django + Gunicorn)
- ✅ Worker Celery
- ✅ Celery Beat (planificateur)
- ✅ Base de données PostgreSQL
- ✅ Cache Redis

#### 4. Variables d'environnement

Configurer dans le dashboard Render :
- `SECRET_KEY` : Généré automatiquement
- `EMAIL_HOST_USER` : Votre email SMTP
- `EMAIL_HOST_PASSWORD` : Mot de passe/API key
- Autres selon besoins

### Déploiement Docker générique

#### VPS/Serveur dédié

```bash
# 1. Cloner sur le serveur
git clone https://github.com/Starland9/EneoNewsletter.git
cd EneoNewsletter

# 2. Configurer l'environnement
nano .env  # Éditer les variables

# 3. Lancer en production
docker-compose up -d

# 4. Initialiser
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py createsuperuser
```

#### Avec Nginx (recommandé)

```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        proxy_pass http://localhost:10000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /chemin/vers/staticfiles/;
    }
}
```

### Checklist de mise en production

- [ ] `DEBUG=False` dans `.env`
- [ ] `SECRET_KEY` unique et sécurisée
- [ ] `ALLOWED_HOSTS` configuré avec votre domaine
- [ ] Base de données PostgreSQL en production
- [ ] Redis en production
- [ ] Serveur SMTP configuré et testé
- [ ] HTTPS configuré (Let's Encrypt recommandé)
- [ ] Sauvegardes automatiques de la base de données
- [ ] Monitoring des logs (Sentry, etc.)
- [ ] Variables sensibles sécurisées (pas dans le code)

---

## 🧪 Tests

### Lancer les tests

```bash
# Tous les tests
docker-compose exec web python manage.py test

# Tests d'une app spécifique
docker-compose exec web python manage.py test newsletter
docker-compose exec web python manage.py test coupure

# Avec couverture
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
```

### Structure des tests

Les tests sont organisés dans chaque application :
- `newsletter/tests.py` : Tests de l'application newsletter
- `coupure/tests.py` : Tests de l'application coupure

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

### 1. Fork & Clone

```bash
git clone https://github.com/votre-username/EneoNewsletter.git
cd EneoNewsletter
```

### 2. Créer une branche

```bash
git checkout -b feature/ma-nouvelle-fonctionnalite
```

### 3. Développer

- Suivre les conventions de code Django
- Ajouter des tests pour les nouvelles fonctionnalités
- Mettre à jour la documentation si nécessaire

### 4. Commit & Push

```bash
git add .
git commit -m "feat: description de la fonctionnalité"
git push origin feature/ma-nouvelle-fonctionnalite
```

### 5. Pull Request

Créez une Pull Request avec :
- Description détaillée des changements
- Captures d'écran si applicable
- Référence aux issues concernées

### Conventions de commit

Utiliser [Conventional Commits](https://www.conventionalcommits.org/) :
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage
- `refactor:` Refactorisation
- `test:` Ajout de tests
- `chore:` Tâches de maintenance

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

```
MIT License

Copyright (c) 2024 Landry Simo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Auteur

**Landry Simo**

- 📧 Email : [landrysimo99@gmail.com](mailto:landrysimo99@gmail.com)
- 💼 GitHub : [@Starland9](https://github.com/Starland9)

---

## 🙏 Remerciements

- **Eneo Cameroun** pour le contexte du projet
- La communauté **Django** pour le framework exceptionnel
- Les contributeurs de **Celery** pour la gestion des tâches asynchrones
- Tous les contributeurs open-source des bibliothèques utilisées

---

<div align="center">

**⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile !**

*Développé avec ❤️ pour améliorer la communication avec les abonnés Eneo*

</div>
