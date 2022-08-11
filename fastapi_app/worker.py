import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from dramatiq.encoder import JSONEncoder

encoder = JSONEncoder()
backend = RedisBackend(encoder=encoder)
broker = RedisBroker(host="localhost", port=6379)

broker.add_middleware(Results(backend=backend))

broker.declare_queue("queue2")

dramatiq.set_broker(broker)
dramatiq.set_encoder(encoder)
