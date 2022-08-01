from flask import Flask,jsonify,request
from models.MlModel import  MlModel
from tools.celery import make_celery
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
    
# Config
app.config.update(CELERY_CONFIG={
    'broker_url': 'redis://localhost:6379',
    'result_backend': 'redis://localhost:6379',
},)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Abc1234!,@localhost/cognitus_task'

# app & database
celery = make_celery(app)
db = SQLAlchemy(app=app)
dbEngine = db.create_engine( 'mysql+pymysql://root:Abc1234!,@localhost/cognitus_task',{})

# Table
class LabeledData(db.Model):
    __tablename__ = "labeled_data"
    id = db.Column("id",db.Integer(),primary_key=True)
    text = db.Column("text",db.String(100))
    label = db.Column("label",db.String(40))

# Query's
allDataQuery = LabeledData.query.statement

# Model
model = MlModel(allDataQuery,dbEngine)

# Handler's
@celery.task(name='flask_app.app.handleTrain')
def handleTrain():
    model.train()
    return 1

def handlePredict(text):
    result = model.predict(text)
    data = {"result_1":result.tolist()[0][0],"result_2":result.tolist()[0][1]}
    return data

# Router's
@app.route('/train')
def train():
    handleTrain.delay()
    return jsonify({"status":"success"})

@app.route('/predict')
def predict():
    args = request.args
    user_text = args.get("user_text")
    result = handlePredict(user_text)
    return jsonify({"data":result})


if __name__ == '__main__':
    app.run(debug=True)
