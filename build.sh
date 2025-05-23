#!/bin/bash
# Sortir en cas d'erreur
set -o errexit

# Installer les dépendances système
apt-get update
apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
pip install --upgrade pip
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --noinput --clear

# Appliquer les migrations
python manage.py migrate --noinput
