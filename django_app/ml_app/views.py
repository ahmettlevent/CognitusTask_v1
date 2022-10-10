from .models import LabeledData
from rest_framework import viewsets
import requests
from django.http import JsonResponse
from django.conf import settings
from .serializers import LabeledDataSerializer


class LabeledDataViewSet(viewsets.ModelViewSet):
    queryset = LabeledData.objects.all()
    serializer_class = LabeledDataSerializer


def train(request):
    response = requests.get(f'{settings.ALGORITHM_URL}/train')
    return JsonResponse(response.json())


def predict(request):
    text = request.GET["user_text"]
    response = requests.get(
        f'{settings.ALGORITHM_URL}/predict?user_text={text}')
    return JsonResponse(response.json())
