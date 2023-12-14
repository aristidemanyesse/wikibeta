from predictionApp.models import *
from fixtureApp.models import *

    
def prediction(match):        
    if len( match.away.get_last_matchs(match, edition = True)) < 4 or len( match.home.get_last_matchs(match, edition = True)) < 4:
        return
    
    home = match.home.get_team_profile(match)
    away = match.away.get_team_profile(match)
        
    if (home.dynamique >= 12  and  away.defense <= 5):
        Prediction.objects.create(
            mode = ModePrediction.get("M1"),
            type = TypePrediction.get("1X"),
            match = match,
            pct = 0.85
        )
    
    home_maitrise = match.home.maitrise(match)
    away_maitrise = match.away.maitrise(match)
    if home_maitrise >= away_maitrise + 4 and home.attack >= away.attack + 3:
        Prediction.objects.create(
            mode = ModePrediction.get("M1"),
            type = TypePrediction.get("1X"),
            match = match,
            pct = 85
        )
            
        
    if (home.defense < 8 and away.defense < 7):
        Prediction.objects.create(
            mode = ModePrediction.get("M1"),
            type = TypePrediction.get("p1_5"),
            match = match,
            pct = 0.85
        )

