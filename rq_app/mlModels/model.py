import pandas as pd
import pickle
from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn.metrics import precision_score, accuracy_score, recall_score


class MlModel():
    def __init__(self,statement,dbEngine) -> None:
        self.text, self.label = self.create_data(statement,dbEngine)
    
    def create_data(self,statement,engine):
        df = pd.read_sql_query(statement,engine)
        return df['text'].tolist(), df['label'].tolist()

    def tfidf(self,data, ma = 0.6, mi = 0.0001):
        tfidf_vectorize = TfidfVectorizer()
        tfidf_data = tfidf_vectorize.fit_transform(data)
        return tfidf_data, tfidf_vectorize

    def test_SVM(self,x_train, x_test, y_train, y_test):
        SVM = SVC(kernel = 'linear', probability=True)
        SVMClassifier = SVM.fit(x_train, y_train)
        predictions = SVMClassifier.predict(x_test)
        a = accuracy_score(y_test, predictions)
        p = precision_score(y_test, predictions, average = 'weighted')
        r = recall_score(y_test, predictions, average = 'weighted')
        return SVMClassifier, a, p, r

    def dump_model(self,model, file_output):
        pickle.dump(model, open(f"./tmp/{file_output}", 'wb'))

    def load_model(self,file_input):
        return pickle.load(open(f"./tmp/{file_input}", 'rb'))
    
    def train(self):
        training, vectorizer = self.tfidf(self.text)
        x_train, x_test, y_train, y_test = cross_validation.train_test_split(training, self.label, test_size = 0.25, random_state = 0)
        model, accuracy, precision, recall = self.test_SVM(x_train, x_test, y_train, y_test)
        self.dump_model(model, 'model.pickle')
        self.dump_model(vectorizer, 'vectorizer.pickle')
        return 1

    def predict(self,user_text):
        model = self.load_model('model.pickle')
        vectorizer = self.load_model('vectorizer.pickle')
        tdifd = vectorizer.transform([user_text])
        result = model.predict_proba(tdifd)
        return result
