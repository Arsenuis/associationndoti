#!/bin/bash
echo "Starting Django application..."

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start gunicorn
echo "Starting gunicorn on port ${PORT:-8000}..."
gunicorn blog_projet.wsgi:application --bind 0.0.0.0:${PORT:-8000}