from pydantic import BaseModel

class MessageId(BaseModel):
    message : dict

class HelloUser(BaseModel):
    detail: str
    message : dict  

class Result(BaseModel):
    detail: str
    x:float
    y:float