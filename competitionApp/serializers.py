
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


class RankingSerializer(ModelSerializer):
    class Meta:
        model = Ranking
        fields = '__all__'

class LigneRankingSerializer(ModelSerializer):
    class Meta:
        model = LigneRanking
        fields = '__all__'

class CompetitionStatSerializer(ModelSerializer):
    class Meta:
        model = CompetitionStat
        fields = '__all__'