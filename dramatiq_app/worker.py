import dramatiq
from dramatiq.encoder import JSONEncoder
from dramatiq.results import Results
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results.backends import RedisBackend
from tasks import hello_user


encoder = JSONEncoder()
backend = RedisBackend(encoder=encoder)
broker = RedisBroker(host="localhost", port=6379)

broker.add_middleware(Results(backend=backend,store_results=True,result_ttl=99999))

broker.declare_actor(hello_user)
broker.declare_queue("queue2")

dramatiq.set_broker(broker)
dramatiq.set_encoder(encoder)
