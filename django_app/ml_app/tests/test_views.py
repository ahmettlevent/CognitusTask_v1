from django.test import  TestCase
from rest_framework.test import RequestsClient

class TestViews(TestCase):
    def setUp(self) :
        self.client = RequestsClient()
    
    def test_prediction(self):
        request = self.client.get('http://testserver/predict?user_text=olumlu')
        self.assertEquals(request.status_code,200)

    def test_train(self):
        request = self.client.get('http://testserver/train/')
        self.assertEquals(request.status_code,200)