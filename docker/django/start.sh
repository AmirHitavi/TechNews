#!/bin/sh

set -o errexit
set -o nounset

cd core


python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py migrate django_celery_beat --no-input
python manage.py collectstatic --no-input

exec python manage.py runserver 0.0.0.0:8000