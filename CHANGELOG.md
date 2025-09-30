# Changelog

Tous les changements notables apportés au projet **EneoNewsletter** seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### Ajouté
- Documentation professionnelle complète (README.md)
- Fichier LICENSE (MIT)
- Guide de contribution (CONTRIBUTING.md)
- Fichier d'exemple de configuration (.env.example)
- Changelog pour suivre les versions

## [1.0.0] - 2024

### Ajouté
- Application de gestion de newsletters avec Django
- Système d'abonnement et de désinscription
- Envoi programmé d'emails avec Celery Beat
- Interface d'administration Django personnalisée
- Gestion des coupures d'électricité programmées
- Récupération automatique des coupures via API Eneo
- Notifications ciblées par quartier
- Templates d'emails personnalisables et responsive
- Support PostgreSQL pour le stockage des données
- Cache Redis pour les performances
- Déploiement conteneurisé avec Docker et Docker Compose
- Configuration pour déploiement sur Render
- Support multi-langue (Français)
- Gestion des fuseaux horaires (Africa/Douala)
- Import/export CSV des abonnés
- Système de logs et d'historique

### Sécurité
- Authentification sécurisée pour l'interface admin
- Configuration des variables sensibles via environnement
- Support HTTPS recommandé pour la production

---

## Format des versions

Ce projet suit le [Versioning Sémantique](https://semver.org/lang/fr/) :
- MAJOR : changements incompatibles avec les versions précédentes
- MINOR : ajout de fonctionnalités rétrocompatibles
- PATCH : corrections de bugs rétrocompatibles

## Types de changements

- `Ajouté` : pour les nouvelles fonctionnalités
- `Modifié` : pour les changements dans les fonctionnalités existantes
- `Obsolète` : pour les fonctionnalités qui seront bientôt supprimées
- `Supprimé` : pour les fonctionnalités maintenant supprimées
- `Corrigé` : pour les corrections de bugs
- `Sécurité` : en cas de vulnérabilités

---

Pour les versions détaillées, voir [les tags](https://github.com/Starland9/EneoNewsletter/tags) sur GitHub.
