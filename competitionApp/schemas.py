from graphene_django_extras import  DjangoSerializerType
from .serializers import *
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

class PaysType(DjangoSerializerType):
    class Meta:
        serializer_class = PaysSerializer
        description = " Type definition for a single Pays "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "code": ("exact",),
            "name": ("icontains", ),
        }


class TypeCompetitionType(DjangoSerializerType):
    class Meta:
        serializer_class = TypeCompetitionSerializer
        description = " Type definition for a single TypeCompetition "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "name": ("exact",),
            "etiquette": ("icontains", ),
        }


class CompetitionType(DjangoSerializerType):
    class Meta:
        serializer_class = CompetitionSerializer
        description = " Type definition for a single Competition "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "identifiant": ("exact",),
            "code": ("exact",),
            "name": ("icontains",),
            "pays__id": ("exact",),
            "type__id": ("exact",),
        }


class EditionType(DjangoSerializerType):
    class Meta:
        serializer_class = EditionSerializer
        description = " Type definition for a single Edition "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "name": ("icontains",),
        }


class EditionCompetitionType(DjangoSerializerType):
    class Meta:
        serializer_class = EditionCompetitionSerializer
        description = " Type definition for a single EditionCompetition "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "edition__id": ("exact",),
            "competition__id": ("exact",),
            "start_date": ("lt", "lte", "gt", "gte" ),
            "finish_date": ("lt", "lte", "gt", "gte" ),
            "is_finished": ("exact", ),
        }


class CompetitionStatType(DjangoSerializerType):
    class Meta:
        serializer_class = CompetitionStatSerializer
        description = " Type definition for a single CompetitionStat "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "edition__id": ("exact",),
            "ranking__id": ("exact",),
        }


class RankingType(DjangoSerializerType):
    class Meta:
        serializer_class = RankingSerializer
        description = " Type definition for a single Ranking "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "edition__id": ("exact",),
            "date": ("lt", "lte", "gt", "gte" ),
        }


class LigneRankingType(DjangoSerializerType):
    class Meta:
        serializer_class = LigneRankingSerializer
        pagination = LimitOffsetGraphqlPagination(default_limit=25, ordering="-ranking__created_at")
        description = " Type definition for a single LigneRanking "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "ranking__id": ("exact",),
            "ranking__date": ("exact", "lt", "lte", "gt", "gte"),
            "team__id": ("exact",),
        }
