from rest_framework import serializers
from .models import LabeledData

class LabeledDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LabeledData
        fields = ['text', 'label']
