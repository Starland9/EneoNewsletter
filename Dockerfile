# Étape 1: Utiliser une image Python officielle comme base
FROM python:3.11-slim

# Étape 2: Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Étape 3: Créer et définir le répertoire de travail
WORKDIR /app

# Étape 4: Installer les dépendances système nécessaires
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Étape 5: Copier les fichiers de dépendances
COPY requirements.txt .

# Étape 6: Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Étape 7: Copier le projet
COPY . .

# Étape 8: Exposer le port 10000
EXPOSE 10000

# Étape 9: Commande de démarrage
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput --clear && gunicorn --bind 0.0.0.0:10000 EneoNewsletter.wsgi"]