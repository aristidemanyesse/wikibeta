
from .models import *
from rest_framework.serializers import ModelSerializer


class MatchSerializer(ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

class GoalSerializer(ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
