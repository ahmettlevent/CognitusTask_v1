from time import sleep
from mlModels.model import MlModel
from database import engine,SessionLocal
from models import LabeledData
from redis import Redis
from rq.decorators import job


session = SessionLocal()
allDataQueryStatement = session.query(LabeledData).statement
mlModel = MlModel(allDataQueryStatement,engine)
redis_conn = Redis("localhost",6379)

@job(['high',"low"], connection=redis_conn, timeout=5)
def predict_model(user_text):
    res = mlModel.predict(user_text)
    if res[0][0].size != 0 and res[0][1].size != 0:
        return {"x":res[0][0],"y":res[0][1],"status":"Success"}
    else:
        return {"status":"Error"}

@job('low', connection=redis_conn)
def train_model():
    mlModel.train()
    return "Model Trained"
