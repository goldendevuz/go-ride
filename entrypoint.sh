#!/bin/sh
set -e

echo "🔄 Running database migrations..."
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput

echo "📦 Collecting static files..."
# python manage.py collectstatic --noinput --clear

echo "🚀 Starting: $@"
exec "$@"