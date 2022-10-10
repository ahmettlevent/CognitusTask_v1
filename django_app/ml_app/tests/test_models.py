from django.test import TestCase
from ml_app.models import LabeledData


class LabeledDataTestCase(TestCase):
    def setUp(self):
        ...

    def test_should_create_and_get_labeledData(self):
        LabeledData.objects.create(text="olabilir", label="confirmation_Yes")
        data = LabeledData.objects.get(text="olabilir")
        self.assertEqual(str(data.text), "olabilir")
        self.assertEqual(str(data.label), "confirmation_Yes")
