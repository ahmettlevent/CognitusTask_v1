from huey import RedisExpireHuey
from mlModels.model import MlModel
from database import engine,SessionLocal
from models import LabeledData

huey = RedisExpireHuey(name="huey",host="localhost",port=6379 )

session = SessionLocal()
allDataQueryStatement = session.query(LabeledData).statement
model = MlModel(allDataQueryStatement,engine)

@huey.task(name="predict_model",id="train_model")
def predict_model(user_text):
    res = model.predict(user_text)

    if res[0][0].size != 0 and res[0][1].size != 0:
        return {"x":res[0][0],"y":res[0][1],"status":"Success"}
    else:
        return {"status":"Error"}


@huey.task(name="train_model")
def train_model():
    model.train()
    return 1