web: gunicorn puzzle:app
worker: celery --app=puzzle.celery worker --loglevel=info --without-gossip --without-mingle --without-heartbeat
