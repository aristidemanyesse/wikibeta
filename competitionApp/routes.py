
from .schemas import *
import graphene


class competitionAppQuery(object):
    search_pays                   = PaysType.ListField(action=graphene.String(default_value="search_pays"))
    search_type_competition       = TypeCompetitionType.ListField(action=graphene.String(default_value="search_officine_pays"))
    search_competition            = CompetitionType.ListField(action=graphene.String(default_value="search_ligne_pays"))
    search_reponse                = EditionType.ListField(action=graphene.String(default_value="search_reponse"))
    search_edition_competition    = EditionCompetitionType.ListField(action=graphene.String(default_value="search_ligne_reponse"))

    
class competitionAppMutation(object):
    create_pays               = PaysType.CreateField()
    update_pays               = PaysType.UpdateField()
    
    create_type_competition   = TypeCompetitionType.CreateField()
    update_type_competition   = TypeCompetitionType.UpdateField()
    
    create_competition        = CompetitionType.CreateField()
    update_competition        = CompetitionType.UpdateField()
    
    create_edition            = EditionType.CreateField()
    update_edition            = EditionType.UpdateField()
    
    create_edition_competiton = EditionCompetitionType.CreateField()
    update_edition_competiton = EditionCompetitionType.UpdateField()