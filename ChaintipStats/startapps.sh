#!/bin/bash

redis-server &
celery -A ChaintipStats worker &
celery -A ChaintipStats beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler &
celery flower -A ChaintipStats --address=127.0.0.1 --port=5555 &
python3 manage.py runserver --insecure 0.0.0.0:8000