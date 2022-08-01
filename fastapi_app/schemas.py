from pydantic import BaseModel

class UserText(BaseModel):
    text : str

class Train(BaseModel):
    detail: str

class Prediction(BaseModel):
    detail: str
    x:float
    y:float