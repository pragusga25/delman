#!/bin/sh

set -e

# Wait for database to be ready
while ! nc -z db 5432; do
  echo "Waiting for database..."
  sleep 2
done

echo "Database is ready"

python -m flask db migrate -m "latest migrations"

echo "Running database migrations..."
python -m flask db upgrade

# Seed database with a check
echo "Checking and seeding database if necessary..."
python seed.py --check

# Start the application
echo "Starting the application..."
exec python -m gunicorn -w 4 -b 0.0.0.0:3000 main:app
