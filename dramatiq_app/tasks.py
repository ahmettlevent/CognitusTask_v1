from celery import Task
from worker import app
from mlModels.model import MlModel
from database import engine,SessionLocal
from models import LabeledData

session = SessionLocal()
allDataQueryStatement = session.query(LabeledData).statement


class PredictTask(Task):
    abstract = True
    mlModel = None

    def __init__(self):
        super().__init__()
        self.mlModel = MlModel(allDataQueryStatement,engine)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

class TrainTask(Task):
    abstract = True
    mlModel = None

    def __init__(self):
        super().__init__()
        self.mlModel = MlModel(allDataQueryStatement,engine)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

@app.task(ignore_result=False,
          name="predict_model",
          bind=True,
          base=PredictTask)
def predict_model(self, data):
    res = self.mlModel.predict(data["user_text"])
    if res[0][0].size != 0 and res[0][1].size != 0:
        return {"x":res[0][0],"y":res[0][1],"status":"Success"}
    else:
        return {"status":"Error"}


@app.task(ignore_result=False,
          name="train_model",
          bind=True,
          base=TrainTask)
def train_model(self):
    self.mlModel.train()
    return 1