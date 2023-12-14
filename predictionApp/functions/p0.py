from predictionApp.models import *
from fixtureApp.models import *
from math import sqrt


def prediction(match):   
    GF = 2.2
    GA = 0.5     
    before_home = match.home.get_before_stats(match)
    before_away = match.away.get_before_stats(match)
    home = sqrt(before_home.avg_goals_scored * before_away.avg_goals_conceded)
    away = sqrt(before_home.avg_goals_conceded * before_away.avg_goals_scored)
    
    if (before_home.avg_goals_scored + before_away.avg_goals_conceded + before_home.avg_goals_conceded + before_away.avg_goals_scored) / 4 > GF:
        Prediction.objects.create(
            mode = ModePrediction.get("M0"),
            type = TypePrediction.get("p1_5"),
            match = match,
            pct = 95
        )
        
    elif home > GF:
        Prediction.objects.create(
            mode = ModePrediction.get("M0"),
            type = TypePrediction.get("HG"),
            match = match,
            pct = 85
        )
        
    # elif away > GF:
    #     PredictionTest.objects.create(
    #         mode = ModePrediction.get("M0"),
    #         type = TypePrediction.get("AG"),
    #         match = match,
    #         pct = 85
    #     )

