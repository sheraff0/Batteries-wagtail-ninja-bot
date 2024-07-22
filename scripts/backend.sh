#!/bin/bash
set -euo pipefail

#python manage.py collectstatic --noinput
#python manage.py migrate --noinput
#python manage.py create_default_superuser

if [ -z ${DEBUG} ];
then
  echo "Starting with Gunicorn"
  gunicorn config.wsgi:application \
    -b 0.0.0.0:8000 --threads 2 \
    --workers 4 \
    #-k uvicorn.workers.UvicornWorker
else
  echo "Starting with Django dev server"
  python -u manage.py runserver 0.0.0.0:8000
fi
