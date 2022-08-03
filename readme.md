## Run Commands
- celery -A celery_app.worker worker                                  # celery worker
- python3 app.py                                                      # flask app
- python3 manage.py runserver                                         # django 
- mysql -u root -p                                                    # mysql 
- uvicorn app:app --host <host_name> --port <port>                    # fastapi


### Redis Local Alternatives

## Redis Task Queue RQ
- - Each worker will process a single job at a time. Within a worker, there is no concurrent processing going on. If you want to perform jobs concurrently, simply start more workers.

# Task Tiger
- - https://github.com/closeio/tasktiger#features"

# Task Master

# Huey

# Kuyruk

# Dramatiq

# Django-carrot

# tasq

# WorQ

## Cloud Based Solutions
- Google Task Queue API
- AWS's Cloud Watch Events
