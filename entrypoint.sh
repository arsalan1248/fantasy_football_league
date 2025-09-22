#!/bin/bash
set -e

# Wait for DB to be ready
echo "Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done
echo "Database is up!"

# Run migrations
echo "Applying migrations..."
python manage.py migrate

# Collect static files (only for production)
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Execute CMD (Gunicorn or runserver)
exec "$@"
