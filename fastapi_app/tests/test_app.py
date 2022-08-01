from fastapi.testclient import TestClient
from ..schemas import *
import pytest
from ..app import app


client = TestClient(app)

@pytest.mark.asyncio
async def test_train():
    response = client.get("/train")
    assert response.status_code == 202
    
@pytest.mark.asyncio
async def test_predict():
    response = client.get("/predict/", params= {"user_text":"test"})
    assert response.status_code == 200
