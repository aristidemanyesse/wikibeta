
from .models import *
from rest_framework.serializers import ModelSerializer


class PaysSerializer(ModelSerializer):
    class Meta:
        model = Pays
        fields = '__all__'

class TypeCompetitionSerializer(ModelSerializer):
    class Meta:
        model = TypeCompetition
        fields = '__all__'

class CompetitionSerializer(ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'


class EditionSerializer(ModelSerializer):
    class Meta:
        model = Edition
        fields = '__all__'

class EditionCompetitionSerializer(ModelSerializer):
    class Meta:
        model = EditionCompetition
        fields = '__all__'