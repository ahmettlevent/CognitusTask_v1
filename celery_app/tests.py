from database import SessionLocal
from models import LabeledData
from sqlalchemy import select
from worker import app


class TestCeleryTasks:
    def setUp(self):
        self.session = SessionLocal()
        
    def test_get_labeledData(self):
        result = self.session.execute(select(LabeledData).where(LabeledData.text=="olmaz")).scalar_one()
        assert str(result.text) == "olmaz"

    def test_prediction(self):
        task = app.send_task("predict_model",args=[dict({"user_text":"olumsuz"})])
        res = task.get()
        assert res["status"] == "Success"
        
    def test_train(self):
        task = app.send_task("train_model")
        res = task.get()
        assert res == 1
