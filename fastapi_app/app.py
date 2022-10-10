from fastapi import FastAPI
from schemas import *
from worker import app as celery_app
from cache import RedisCache

cache = RedisCache("redis", 6379, 1)

app = FastAPI()


@app.get('/train', response_model=Train,  status_code=202)
async def train():
    celery_app.send_task("train_model")
    cache.cleanCache()
    return {"detail": "Processing"}


@app.get('/predict', response_model=Prediction, status_code=200)
def predict(user_text=UserText):
    cache_res = cache.getDataFromCache(user_text)
    res = {"x": 0, "y": 0}

    if None in cache_res:
        task_res = celery_app.send_task(
            "predict_model", args=[dict({"user_text": user_text})]).get()
        cache.addDataToCache(user_text, task_res["x"], task_res["y"])
        res["x"] = task_res["x"]
        res["y"] = task_res["y"]
    else:
        res["x"] = cache_res[0]
        res["y"] = cache_res[1]

    return {'detail': 'Success', 'x': float(res["x"]), 'y': float(res["y"])}
