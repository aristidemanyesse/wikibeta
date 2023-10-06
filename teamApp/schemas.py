from graphene_django_extras import  DjangoSerializerType
from .serializers import *


class TeamType(DjangoSerializerType):
    class Meta:
        serializer_class = TeamSerializer
        description = " Type definition for a single Team "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "pays__id": ("exact",),
            "code": ("exact", ),
            "name": ("icontains", ),
        }



class EditionTeamType(DjangoSerializerType):
    class Meta:
        serializer_class = EditionTeamSerializer
        description = " Type definition for a single EditionTeam "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "edition__id": ("exact",),
            "team__id": ("exact",),
        }

