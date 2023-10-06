
from .models import *
from rest_framework.serializers import ModelSerializer


class ModePredictionSerializer(ModelSerializer):
    class Meta:
        model = ModePrediction
        fields = '__all__'

class TypePredictionSerializer(ModelSerializer):
    class Meta:
        model = TypePrediction
        fields = '__all__'

class PredictionSerializer(ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'


class PredictionScoreSerializer(ModelSerializer):
    class Meta:
        model = PredictionScore
        fields = '__all__'

