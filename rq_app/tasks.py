from mlModels.model import MlModel
from database import engine,SessionLocal
from models import LabeledData
from redis import Redis
from rq.decorators import job

session = SessionLocal()
allDataQueryStatement = session.query(LabeledData).statement
mlModel = MlModel(allDataQueryStatement,engine)

redis_conn = Redis()

@job('low', connection=redis_conn, timeout=5)
def train_model():
    mlModel.train()
    return 1