from pydantic import BaseModel

class UserText(BaseModel):
    text : str

class JobId(BaseModel):
    job_id : str

class Train(BaseModel):
    detail: str
    job_id : str

class TrainResult(BaseModel):
    detail: str
    job_id: str
    result : str

class Prediction(BaseModel):
    detail: str
    job_id: str

class PredictionResult(BaseModel):
    detail: str
    x : str
    y : str