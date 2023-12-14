from coreApp.management.commands.predictionscore import predictscore
from predictionApp.models import *
from fixtureApp.models import *

    
def prediction(match):        
    if len( match.away.get_last_matchs(match, edition = True)) < 4 or len( match.home.get_last_matchs(match, edition = True)) < 4:
        return
    
    scores = predictscore(match)
    test = [x for x in scores if x.home_score == x.away_score]
    if len(test) ==0:
        Prediction.objects.create(
            mode = ModePrediction.get("M3"),
            type = TypePrediction.get("12"),
            match = match,
            pct = 85
        )
