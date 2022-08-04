from fastapi import FastAPI
from redis import Redis
from schemas import *
from cache import RedisCache
from rq import Queue 
from tasks import PicklePrediction

q = Queue("low",connection=Redis("localhost","6379"))
p = PicklePrediction() 
cache = RedisCache("localhost",6379,1)
app = FastAPI()

@app.get('/train',response_model=Train,  status_code=202)
async def train():  
    q.enqueue("tasks.train_model")
    cache.cleanCache()
    return {"detail":"Processing"}
    
@app.get('/predict', response_model=Prediction, status_code=200)
def predict(user_text = UserText):
    cache_res = cache.getDataFromCache(user_text)
    res = {"x":0,"y":0}

    if None in cache_res :
        task_res = p.predict_model(user_text)
        cache.addDataToCache(user_text,task_res["x"],task_res["y"])
        res["x"] = task_res["x"]
        res["y"] = task_res["y"]
    else :
        res["x"] = cache_res[0]
        res["y"] = cache_res[1]

    return {'detail': 'Success','x': float(res["x"]),'y': float(res["y"])}