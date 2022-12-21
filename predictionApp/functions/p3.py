from predictionApp.models import *
from fixtureApp.models import *


def function(edition):
    for match in edition.edition_du_match.all():
        predict(match)
    
    
def predict(match):
    matchs = match.similaires_ppg2()
    if len(matchs) >= 14 :
        moy = 0
        for x in matchs:
            result = x.get_result()
            moy += (result.home_score + result.away_score) / len(matchs)
            
        if (moy >= 2.7):
            for x in [1.5, 2.5, 3.5]:
                p = fish_law_plus(moy, x)
                if p >= 85:
                    Prediction.objects.create(
                        mode = ModePrediction.get("M3"),
                        type = TypePrediction.get("p{}".format(str(x).replace(".", "_"))),
                        match = match,
                        pct = p
                    )
                
                
        if (moy <= 2):
            for x in [1.5, 2.5, 3.5]:
                p = fish_law_moins(moy, x)
                if p >= 85:
                    Prediction.objects.create(
                        mode = ModePrediction.get("M3"),
                        type = TypePrediction.get("m{}".format(str(x).replace(".", "_"))),
                        match = match,
                        pct = p
                    )
                    
        total = 0     
        for x in matchs:
            ppg_home = x.get_home_before_stats().ppg
            ppg_away = x.get_away_before_stats().ppg
            
            result = x.get_result()
            
            if ppg_home == ppg_away :
                total += 1
            elif ppg_home > ppg_away and result.home_score >= result.away_score :
                total += 1
            elif ppg_home < ppg_away and result.home_score <= result.away_score :
                total += 1
        
        p = (total / len(matchs)) * 100
        if p >= 85:
            Prediction.objects.create(
                mode = ModePrediction.get("M3"),
                type = TypePrediction.get("VN_{}".format("Home" if ppg_home >= ppg_away else "Away" )),
                match = match,
                pct = p
            )
                
                