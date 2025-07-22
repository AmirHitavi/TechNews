#!/bin/sh
set -o errexit
set -o nounset

sleep 10

cd /src/core
exec celery -A config.celery beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
