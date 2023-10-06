
from .models import *
from rest_framework.serializers import ModelSerializer


class BookmakerSerializer(ModelSerializer):
    class Meta:
        model = Bookmaker
        fields = '__all__'

class OddsMatchSerializer(ModelSerializer):
    class Meta:
        model = OddsMatch
        fields = '__all__'
