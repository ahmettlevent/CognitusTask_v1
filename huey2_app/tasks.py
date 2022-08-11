from huey import RedisHuey


huey = RedisHuey("ml_app",host="localhost", port=6379)

@huey.task()
def add(a, b):
    return a + b