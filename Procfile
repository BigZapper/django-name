release: python manage.py migrate --noinput
gunicorn tenhay.wsgi:application
web: python tenhay/manage.py runserver 0.0.0.0:$PORT
web: gunicorn tenhay.wsgi --log-file -