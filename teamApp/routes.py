
from .schemas import *
import graphene


class teamAppQuery(object):
    search_team                   = TeamType.ListField(action=graphene.String(default_value="search_team"))
    search_edition_team       = EditionTeamType.ListField(action=graphene.String(default_value="search_edition_team"))

    
class teamAppMutation(object):
    create_team               = TeamType.CreateField()
    update_team               = TeamType.UpdateField()
    
    create_edition_team   = EditionTeamType.CreateField()
    update_edition_team   = EditionTeamType.UpdateField()