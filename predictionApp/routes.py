
from .schemas import *
import graphene


class predictionAppQuery(object):
    search_mode_prediction            = ModePredictionType.ListField(action=graphene.String(default_value="search_mode_prediction"))
    search_type_prediction            = TypePredictionType.ListField(action=graphene.String(default_value="search_officine_mode_prediction"))
    search_prediction                 = PredictionType.ListField(action=graphene.String(default_value="search_ligne_mode_prediction"))
    search_prediction_score           = PredictionScoreType.ListField(action=graphene.String(default_value="search_reponse"))

    
class predictionAppMutation(object)   : 
    create_mode_prediction            = ModePredictionType.CreateField()
    update_mode_prediction            = ModePredictionType.UpdateField()
    
    create_type_prediction            = TypePredictionType.CreateField()
    update_type_prediction            = TypePredictionType.UpdateField()
    
    create_prediction                 = PredictionType.CreateField()
    update_prediction                 = PredictionType.UpdateField()
    
    create_prediction_score           = PredictionScoreType.CreateField()
    update_prediction_score           = PredictionScoreType.UpdateField()