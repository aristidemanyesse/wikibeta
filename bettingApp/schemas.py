from graphene_django_extras import  DjangoSerializerType
from .serializers import *


class BookmakerType(DjangoSerializerType):
    class Meta:
        serializer_class = BookmakerSerializer
        description = " Type definition for a single Bookmaker "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "name": ("icontains",),
            "code": ("exact", ),
        }



class OddsMatchType(DjangoSerializerType):
    class Meta:
        serializer_class = OddsMatchSerializer
        description = " Type definition for a single OddsMatch "
        filter_fields = {
            "id": ("exact", ),
            "deleted": ("exact", ),
            "match__id": ("exact",),
            "booker__id": ("exact",),
        }

