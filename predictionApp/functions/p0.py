from predictionApp.models import *
from fixtureApp.models import *
from math import sqrt


GF = 2.2
GA = 0.5

def function(edition):
    for match in edition.edition_du_match.all():
        predict(match)
    
    
def predict(match):        
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
    
    if home > GF and away > GF:
        Prediction.objects.create(
            mode = ModePrediction.get("M0"),
            type = TypePrediction.get("btts"),
            match = match,
            pct = 85
        )
        Prediction.objects.create(
            mode = ModePrediction.get("M0"),
            type = TypePrediction.get("p1_5"),
            match = match,
            pct = 85
        )
        
    if home < GA and away < GA:
        Prediction.objects.create(
            mode = ModePrediction.get("M0"),
            type = TypePrediction.get("no_btts"),
            match = match,
            pct = 85
        )
        Prediction.objects.create(
            mode = ModePrediction.get("M0"),
            type = TypePrediction.get("m3_5"),
            match = match,
            pct = 85
        )
        
    elif home > GF:
        Prediction.objects.create(
            mode = ModePrediction.get("M0"),
            type = TypePrediction.get("But_Home"),
            match = match,
            pct = 85
        )
        
    elif away > GF:
        Prediction.objects.create(
            mode = ModePrediction.get("M0"),
            type = TypePrediction.get("But_Away"),
            match = match,
            pct = 85
        )

