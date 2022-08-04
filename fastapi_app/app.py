from fastapi import FastAPI
from redis import Redis
from schemas import *
from rq import Queue,Retry
from rq.job import Job

redis_conn = Redis("localhost",6379)
q = Queue("low",connection=redis_conn)
q2 = Queue("high",connection=redis_conn)

app = FastAPI()

def report_success(job, connection, result, *args, **kwargs):
    raise ModuleNotFoundError

def report_failure(job, connection, type, value, traceback):
    raise ModuleNotFoundError

@app.get('/train',response_model=Train,  status_code=202)
async def train():  
    job = q.enqueue("tasks.train_model",result_ttl = 5000,retry=Retry(max=3, interval=[10, 30, 60]))
    return {"detail":"Processing","job_id":job.id}

@app.get('/train_result',response_model=TrainResult,  status_code=202)
async def train(job_id = JobId):  
    job = Job.fetch(job_id, connection=redis_conn)
    detail = job.get_status(refresh=True)
    res = job.result
    return {"detail":str(detail),"result":str(res),"job_id":job_id}

@app.get('/predict', response_model=Prediction, status_code=200)
def predict(user_text = UserText):
    job = q2.enqueue("tasks.predict_model",user_text,result_ttl = 5000,retry=Retry(max=3, interval=[10, 30, 60]) )
    return {'detail': 'Processing',"job_id":job.id}

@app.get('/predict_result', response_model=PredictionResult, status_code=200)
def predict(job_id = JobId):
    job = Job.fetch(job_id, connection=redis_conn)
    detail = job.get_status(refresh=True)
    res = job.result

    if detail != "finished":      
        return {"detail":str(detail),'x': float(0),'y': float(0)}

    return {"detail":str(detail),'x': float(res["x"]),'y': float(res["y"])}