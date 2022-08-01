import redis

class RedisCache():
    def __init__(self,host,port,db) -> None:
        self.r = redis.Redis(host=host,port=port,db=db, charset="utf-8", decode_responses=True)

    def cleanCache(self):
        self.r.flushall()
        return True

    def getDataFromCache(self,text):
        pipe = self.r.pipeline()
        pipe.hget(str(text),str("x"))
        pipe.hget(str(text),str("y"))
        res = pipe.execute()
        return res

    def addDataToCache(self,text,x,y):
        pipe = self.r.pipeline()
        pipe.hset(str(text),str("x"),x)
        pipe.hset(str(text),str("y"),y)
        res = pipe.execute()
        return res