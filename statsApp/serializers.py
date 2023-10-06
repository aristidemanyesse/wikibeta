
from .models import *
from rest_framework.serializers import ModelSerializer


class TypeFactSerializer(ModelSerializer):
    class Meta:
        model = TypeFact
        fields = '__all__'

class FactSerializer(ModelSerializer):
    class Meta:
        model = Fact
        fields = '__all__'

class BeforeMatchStatSerializer(ModelSerializer):
    class Meta:
        model = BeforeMatchStat
        fields = '__all__'


class ResultMatchSerializer(ModelSerializer):
    class Meta:
        model = ResultMatch
        fields = '__all__'


class ExtraInfosMatchSerializer(ModelSerializer):
    class Meta:
        model = ExtraInfosMatch
        fields = '__all__'
        
        
class TeamProfileMatchSerializer(ModelSerializer):
    class Meta:
        model = TeamProfileMatch
        fields = '__all__'