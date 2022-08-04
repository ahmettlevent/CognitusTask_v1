from time import sleep
from redis import Redis
from rq.decorators import job
import pickle

class PicklePrediction:
    def load_model(self,file_input):
        return pickle.load(open(f"./tmp/{file_input}", 'rb'))

    def predict(self,user_text):
        model = self.load_model('model.pickle')
        vectorizer = self.load_model('vectorizer.pickle')
        tdifd = vectorizer.transform([user_text])
        result = model.predict_proba(tdifd)
        return result

    def predict_model(self,user_text):
        print("s")
        res = self.predict(user_text)
        if res[0][0].size != 0 and res[0][1].size != 0:
            return {"x":res[0][0],"y":res[0][1],"status":"Success"}
        else:
            return {"status":"Error"}
