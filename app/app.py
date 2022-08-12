from fastapi import FastAPI
from app_schemas import *
from huey_app.tasks import predict_model,train_model
from huey import RedisHuey

app = FastAPI()
huey = RedisHuey(name="huey",host="localhost",port=6379 )

@app.get('/train',response_model=Train,  status_code=202)
async def train():
    r = train_model()
    return {"detail":"Processing","task_id":r.id}

@app.get('/train_result',response_model=TrainResult,  status_code=202)
async def train(task_id = TaskID):
    res = huey.result(task_id)
    return {"detail":"Successfull","task_id":task_id}
    
@app.get('/predict', response_model=Prediction, status_code=200)
def predict(user_text = UserText):
    r = predict_model(user_text=str(user_text))
    return {'detail': 'Success','task_id':r.id}

@app.get('/predict_result', response_model=PredictionResult, status_code=200)
def predict(task_id = TaskID):
    res = {"x":0,"y":0}
    res = huey.result(task_id)
    print(res["x"])
    return {'detail': 'Success',"task_id":str(task_id),'x': float(res["x"]),'y': float(res["y"])}