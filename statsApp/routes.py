
from .schemas import *
import graphene


class statsAppQuery(object):
    search_type_fact            = TypeFactType.ListField(action=graphene.String(default_value="search_type_fact"))
    search_fact                 = FactType.ListField(action=graphene.String(default_value="search_fact"))
    search_before_match_stat    = BeforeMatchStatType.ListField(action=graphene.String(default_value="search_before_match_stat"))
    search_result_match         = ResultMatchType.ListField(action=graphene.String(default_value="search_result_match"))
    search_extra_infos_match    = ExtraInfosMatchType.ListField(action=graphene.String(default_value="search_extra_infos_match"))
    search_team_profile_match   = TeamProfileMatchType.ListField(action=graphene.String(default_value="search_team_profile_match"))

    
class statsAppMutation(object)  : 
    create_type_fact            = TypeFactType.CreateField()
    update_type_fact            = TypeFactType.UpdateField()
    
    create_fact                 = FactType.CreateField()
    update_fact                 = FactType.UpdateField()
    
    create_before_match_stat    = BeforeMatchStatType.CreateField()
    update_before_match_stat    = BeforeMatchStatType.UpdateField()
    
    create_result_match         = ResultMatchType.CreateField()
    update_result_match         = ResultMatchType.UpdateField()
    
    create_extra_infos_match    = ExtraInfosMatchType.CreateField()
    update_extra_infos_match    = ExtraInfosMatchType.UpdateField()
    
    create_team_profile_match   = TeamProfileMatchType.CreateField()
    update_team_profile_match   = TeamProfileMatchType.UpdateField()