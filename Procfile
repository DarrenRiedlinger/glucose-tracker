web: python glucosetracker/manage.py collectstatic --noinput; newrelic-admin run-program python glucosetracker/manage.py run_gunicorn --settings=settings.heroku -b 0.0.0.0:$PORT
