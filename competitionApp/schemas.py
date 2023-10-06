from graphene_django_extras import  DjangoSerializerType
from .serializers import *


class PaysType(DjangoSerializerType):
    class Meta:
        serializer_class = PaysSerializer
        description = " Type definition for a single Pays "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "utilisateur__id": ("exact",),
            "propagating": ("exact", ),
            "is_finished": ("exact", ),
            "is_satisfied": ("exact", ),
        }



class TypeCompetitionType(DjangoSerializerType):
    class Meta:
        serializer_class = TypeCompetitionSerializer
        description = " Type definition for a single TypeCompetition "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "demande__id": ("exact",),
            "is_valided": ("exact", ),
            "propagated": ("exact", ),
            "officine__id": ("exact",),
            "officine__circonscription__id": ("exact",),
        }


class CompetitionType(DjangoSerializerType):
    class Meta:
        serializer_class = CompetitionSerializer
        description = " Type definition for a single Competition "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "demande__id": ("exact",),
            "produit__id": ("exact",),
            "status": ("exact", ),
        }


class EditionType(DjangoSerializerType):
    class Meta:
        serializer_class = EditionSerializer
        description = " Type definition for a single Edition "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "demande__id": ("exact",),
            "demande__demande__id": ("exact",),
            "demande__officine__id": ("exact",),
        }


class EditionCompetitionType(DjangoSerializerType):
    class Meta:
        serializer_class = EditionCompetitionSerializer
        description = " Type definition for a single EditionCompetition "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "reponse__id": ("exact",),
            "produit__id": ("exact",),
            "status": ("exact", ),
        }
