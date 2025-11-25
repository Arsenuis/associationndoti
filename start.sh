#!/bin/bash
set -e

echo "Starting Django application..."

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start gunicorn with Railway PORT
echo "Starting gunicorn..."
if [ -n "$PORT" ]; then
    echo "Using Railway PORT: $PORT"
    exec gunicorn blog_projet.wsgi:application --bind 0.0.0.0:$PORT
else
    echo "Using default PORT: 8000"
    exec gunicorn blog_projet.wsgi:application --bind 0.0.0.0:8000
fi