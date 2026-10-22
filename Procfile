web: gunicorn --bind 0.0.0.0:$PORT --workers 3 --timeout 120 manage:app
release: flask --app manage.py db upgrade
