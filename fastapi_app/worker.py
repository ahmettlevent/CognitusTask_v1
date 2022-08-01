from celery import Celery

BROKER_URI = "redis://redis:6379"
BACKEND_URI = "redis://redis:6379"

app = Celery(
    'celery_app',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['celery_app.tasks']
)

