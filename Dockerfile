# Utiliser Python 3.10 (plus stable avec Railway)
FROM python:3.10-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Commande de démarrage avec migrations et port fixe
CMD python manage.py migrate && python manage.py collectstatic --noinput && gunicorn blog_projet.wsgi:application --bind 0.0.0.0:${PORT:-8000}