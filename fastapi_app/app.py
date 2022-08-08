from fastapi import FastAPI
from schemas import *
from worker import app as celery_app
from cache import RedisCache

cache = RedisCache("redis",6379,1)

app = FastAPI()

@app.get('/train',response_model=Train,  status_code=202)
async def train():
    return {"detail":"Processing"}
    

@app.get('/predict', response_model=Prediction, status_code=200)
def predict(user_text = UserText):
    res = {"x":0,"y":0}
    return {'detail': 'Success','x': float(res["x"]),'y': float(res["y"])}