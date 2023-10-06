from graphene_django_extras import  DjangoSerializerType
from .serializers import *


class TypeFactType(DjangoSerializerType):
    class Meta:
        serializer_class = TypeFactSerializer
        description = " Type definition for a single TypeFact "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "name": ("exact",),
        }



class FactType(DjangoSerializerType):
    class Meta:
        serializer_class = FactSerializer
        description = " Type definition for a single Fact "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "type__id": ("exact",),
            "match__id": ("exact",),
            "team__id": ("exact",),
        }


class ResultMatchType(DjangoSerializerType):
    class Meta:
        serializer_class = ResultMatchSerializer
        description = " Type definition for a single ResultMatch "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "match__id": ("exact",),
            "result": ("exact",),
        }


class BeforeMatchStatType(DjangoSerializerType):
    class Meta:
        serializer_class = BeforeMatchStatSerializer
        description = " Type definition for a single BeforeMatchStat "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "match__id": ("exact",),
            "team__id": ("exact",),
        }


class ExtraInfosMatchType(DjangoSerializerType):
    class Meta:
        serializer_class = ExtraInfosMatchSerializer
        description = " Type definition for a single ExtraInfosMatch "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "match__id": ("exact",),
        }


class TeamProfileMatchType(DjangoSerializerType):
    class Meta:
        serializer_class = TeamProfileMatchSerializer
        description = " Type definition for a single TeamProfileMatch "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "match__id": ("exact",),
            "team__id": ("exact",),
            "date": ("lt", "lte", "gt", "gte" ),
        }
