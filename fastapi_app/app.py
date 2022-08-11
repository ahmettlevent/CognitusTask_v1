import dramatiq
from fastapi import FastAPI
from schemas import *
from worker import broker,backend

app = FastAPI()

@app.get('/hello_user',response_model=HelloUser,  status_code=202)
async def train(user_name):


    newMessage = dramatiq.Message(queue_name="queue2",actor_name="hello_user",args=(),kwargs={"user_name":user_name},options={})  
    broker.enqueue(newMessage,delay=10000)
    
    
    
    return {"detail":"Processing","message":newMessage.message_id}
    
@app.get('/result', response_model=Result, status_code=200)
def predict(message_id = MessageId):
    result = backend.get_result(message_id)
    print(result)
    res = {"x":0,"y":0}
    return {'detail': 'Success','x': float(res["x"]),'y': float(res["y"])}