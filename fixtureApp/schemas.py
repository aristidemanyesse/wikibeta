from graphene_django_extras import  DjangoSerializerType
from .serializers import *


class MatchType(DjangoSerializerType):
    class Meta:
        serializer_class = MatchSerializer
        description = " Type definition for a single Match "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "date": ("exact", "lt", "lte", "gt", "gte" ),
            "home__id": ("exact", ),
            "away__id": ("exact", ),
            "home__team__id": ("exact", ),
            "away__team__id": ("exact", ),
            "edition__id": ("exact", ),
            "is_finished": ("exact", ),
            "is_predict": ("exact", ),
        }



class GoalType(DjangoSerializerType):
    class Meta:
        serializer_class = GoalSerializer
        description = " Type definition for a single Goal "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
        }
