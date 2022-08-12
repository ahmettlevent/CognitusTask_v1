from pydantic import BaseModel

class UserText(BaseModel):
    text : str

class TaskID(BaseModel):
    task_id : str

class Train(BaseModel):
    detail: str
    task_id : str

class TrainResult(BaseModel):
    detail: str
    task_id : str

class Prediction(BaseModel):
    detail: str
    task_id : str

class PredictionResult(BaseModel):
    detail: str
    task_id : str
    x:float
    y:float
