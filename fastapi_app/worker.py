import redis
from rq import Worker, Queue, Connection
from celery import Celery

BROKER_URI = "redis://localhost:6379"
BACKEND_URI = "redis://localhost:6379"

app = Celery(
    'celery_app',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['celery_app.tasks']
)

 
listen = ['default']
conn_redis = redis.from_url(BACKEND_URI)

if __name__ == '__main__':
    with Connection(conn_redis):
        worker = Worker(list(map(Queue, listen)))
    worker.work()