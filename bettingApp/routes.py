
from .schemas import *
import graphene


class bettingAppQuery(object):
    search_bookmaker                = BookmakerType.ListField(action=graphene.String(default_value="search_bookmaker"))
    search_odds_match               = OddsMatchType.ListField(action=graphene.String(default_value="search_odds_match"))

    
class bettingAppMutation(object)    : 
    create_bookmaker                = BookmakerType.CreateField()
    update_bookmaker                = BookmakerType.UpdateField()
    
    create_odds_match               = OddsMatchType.CreateField()
    update_odds_match               = OddsMatchType.UpdateField()