
from .models import *
from rest_framework.serializers import ModelSerializer


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class EditionTeamSerializer(ModelSerializer):
    class Meta:
        model = EditionTeam
        fields = '__all__'
