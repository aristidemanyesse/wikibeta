
from .schemas import *
import graphene


class competitionAppQuery(object):
    search_pays                         = PaysType.ListField(action=graphene.String(default_value="search_pays"))
    search_type_competition             = TypeCompetitionType.ListField(action=graphene.String(default_value="search_type_competition"))
    search_competition                  = CompetitionType.ListField(action=graphene.String(default_value="search_competition"))
    search_edition                      = EditionType.ListField(action=graphene.String(default_value="search_edition"))
    search_edition_competition          = EditionCompetitionType.ListField(action=graphene.String(default_value="search_edition_competition"))
    search_ranking                      = RankingType.ListField(action=graphene.String(default_value="search_ranking"))
    search_ligne_ranking                = LigneRankingType.ListField(action=graphene.String(default_value="search_ligne_ranking"))
    search_competition_stat             = CompetitionStatType.ListField(action=graphene.String(default_value="search_competition_stat"))

    
class competitionAppMutation(object)    : 
    create_pays                         = PaysType.CreateField()
    update_pays                         = PaysType.UpdateField()
    
    create_type_competition             = TypeCompetitionType.CreateField()
    update_type_competition             = TypeCompetitionType.UpdateField()
    
    create_competition                  = CompetitionType.CreateField()
    update_competition                  = CompetitionType.UpdateField()
    
    create_edition                      = EditionType.CreateField()
    update_edition                      = EditionType.UpdateField()
    
    create_edition_competiton           = EditionCompetitionType.CreateField()
    update_edition_competiton           = EditionCompetitionType.UpdateField()
    
    create_ranking                      = RankingType.CreateField()
    update_ranking                      = RankingType.UpdateField()
    
    create_ligne_ranking                = LigneRankingType.CreateField()
    update_ligne_ranking                = LigneRankingType.UpdateField()
    
    create_competition_stat             = CompetitionStatType.CreateField()
    update_competition_stat             = CompetitionStatType.UpdateField()