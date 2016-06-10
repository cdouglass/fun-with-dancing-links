web: gunicorn puzzle:app
worker: celery --app=puzzle.celery worker --loglevel=info
