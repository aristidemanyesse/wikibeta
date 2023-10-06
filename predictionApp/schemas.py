from graphene_django_extras import  DjangoSerializerType
from .serializers import *


class ModePredictionType(DjangoSerializerType):
    class Meta:
        serializer_class = ModePredictionSerializer
        description = " Type definition for a single ModePrediction "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "name": ("exact",),
        }



class TypePredictionType(DjangoSerializerType):
    class Meta:
        serializer_class = TypePredictionSerializer
        description = " Type definition for a single TypePrediction "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "name": ("exact",),
            "code": ("exact", ),
        }


class PredictionType(DjangoSerializerType):
    class Meta:
        serializer_class = PredictionSerializer
        description = " Type definition for a single Prediction "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "mode__id": ("exact",),
            "type__id": ("exact",),
            "match__id": ("exact",),
            "pct": ("exact", ),
            "is_checked": ("exact", ),
        }


class PredictionScoreType(DjangoSerializerType):
    class Meta:
        serializer_class = PredictionScoreSerializer
        description = " Type definition for a single PredictionScore "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "match__id": ("exact",),
            "pct": ("exact", ),
            "is_checked": ("exact", ),
        }
