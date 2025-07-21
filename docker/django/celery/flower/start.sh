#!/bin/sh
set -o errexit
set -o nounset

cd /src/core 
exec celery -A config.celery  -b "${CELERY_BROKER_URL}" flower --basic-auth="${CELERY_FLOWER_USER}":"${CELERY_FLOWER_PASSWORD}"