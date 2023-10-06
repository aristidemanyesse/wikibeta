
from .schemas import *
import graphene


class fixtureAppQuery(object):
    search_match                   = MatchType.ListField(action=graphene.String(default_value="search_match"))
    search_goal       = GoalType.ListField(action=graphene.String(default_value="search_goal"))

    
class fixtureAppMutation(object):
    create_match               = MatchType.CreateField()
    update_match               = MatchType.UpdateField()
    
    create_goal   = GoalType.CreateField()
    update_goal   = GoalType.UpdateField()