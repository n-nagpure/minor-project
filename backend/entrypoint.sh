#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_data || true

exec gunicorn pricecompare.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
