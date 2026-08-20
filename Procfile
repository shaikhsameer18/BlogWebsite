release: python mywebsite/manage.py migrate --noinput
web: gunicorn mywebsite.wsgi --pythonpath mywebsite --bind 0.0.0.0:$PORT
