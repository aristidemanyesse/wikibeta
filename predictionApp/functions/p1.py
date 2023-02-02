from predictionApp.models import *
from fixtureApp.models import *

def function(edition):
    for match in edition.edition_du_match.all():
        if match.prediction_match.all().count() == 0 :
            predict(match)
    
    
def predict(match):        
    matchs = match.confrontations_directes(20)
    if len(matchs) >= 7 :
        moy = 0
        for x in matchs:
            result = x.get_result()
            moy += (result.home_score + result.away_score) / len(matchs)
            
        
        if (moy >= 2.7):
            for x in [1.5, 2.5, 3.5]:
                p = fish_law_plus(moy, x)
                if p >= 85:
                    Prediction.objects.create(
                        mode = ModePrediction.get("M1"),
                        type = TypePrediction.get("p{}".format(str(x).replace(".", "_"))),
                        match = match,
                        pct = p
                    )
                
                
        if (moy <= 2):
            for x in [2.5, 3.5]:
                p = fish_law_moins(moy, x)
                if p >= 85:
                    Prediction.objects.create(
                        mode = ModePrediction.get("M1"),
                        type = TypePrediction.get("m{}".format(str(x).replace(".", "_"))),
                        match = match,
                        pct = p
                    )

