# EneoNewsletter

Application de gestion de newsletter avec Django, Celery et Redis. Cette application permet de gérer les abonnements aux newsletters, d'envoyer des emails programmés et de suivre les statistiques d'envoi.

## Fonctionnalités

- Gestion des abonnés et des listes de diffusion
- Envoi d'emails programmés avec Celery Beat
- Tableau de bord d'administration Django
- Stockage des données dans PostgreSQL
- Mise en cache avec Redis
- Déploiement conteneurisé avec Docker

## Prérequis

- Docker et Docker Compose
- Python 3.8+
- Un client SMTP pour l'envoi d'emails

## Installation

1. Clonez le dépôt :
   ```bash
   git clone [URL_DU_DEPOT]
   cd EneoNewsletter
   ```

2. Créez un fichier `.env` à la racine du projet avec les variables d'environnement nécessaires. Vous pouvez utiliser le fichier `.env.example` comme modèle.

3. Construisez et lancez les conteneurs :
   ```bash
   docker-compose up --build
   ```

4. Effectuez les migrations de la base de données :
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. Créez un superutilisateur pour accéder à l'interface d'administration :
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## Structure du projet

- `/EneoNewsletter` : Configuration principale du projet Django
- `/newsletter` : Application principale de gestion des newsletters
- `/templates` : Modèles de templates HTML
- `/coupure` : Gestion des coupures (si applicable)

## Variables d'environnement

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```
SECRET_KEY=votre_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre_email
EMAIL_HOST_PASSWORD=votre_mot_de_passe
EMAIL_DEFAULT_FROM=noreply@example.com

# Redis
REDIS_URL=redis://redis:6379/0

# Autres
TIME_ZONE=Africa/Douala
```

## Démarrage

1. Démarrez les services :
   ```bash
   docker-compose up -d
   ```

2. Accédez à l'application :
   - Interface web : http://localhost:10000
   - Admin : http://localhost:10000/admin

## Tâches planifiées

L'application utilise Celery Beat pour les tâches planifiées. Les tâches courantes incluent :

- Envoi des newsletters programmées
- Nettoyage des anciens logs
- Mises à jour des statistiques

## Déploiement

Pour le déploiement en production, assurez-vous de :

1. Mettre `DEBUG=False` dans le fichier `.env`
2. Configurer un vrai serveur SMTP
3. Mettre à jour `ALLOWED_HOSTS` avec votre domaine
4. Configurer un reverse proxy (Nginx/Apache) avec HTTPS

## Licence

[À spécifier selon la licence choisie]

## Auteur

Landry Simo - [Contact](mailto:landrysimo99@gmail.com)
---

*Ce projet a été développé avec ❤️ pour Eneo*
