from predictionApp.models import *
from fixtureApp.models import *
from competitionApp.models import *
        
def function(edition):
    for match in edition.edition_du_match.all():
        if match.prediction_match.all().count() == 0 :
            predict(match)
    
    
def predict(match):
    matchs = match.similaires_betting(10)
    datas = {"home":0, "away":0, "draw":0, "1_5":0, "2_5":0, "3_5":0}
    if len(matchs) >= 5 :
        moy = 0
        for match in matchs:
            result = match.get_result()
            if result is None:
                test += 1
                continue
                # datas["home"] += 1 if result.home_score > result.away_score else 0
                # datas["away"] += 1 if result.home_score < result.away_score else 0
                # datas["draw"] += 1 if result.home_score == result.away_score else 0
                # datas["1_5"] += 1 if result.home_score + result.away_score > 1.5 else 0
                # datas["2_5"] += 1 if result.home_score + result.away_score > 2.5 else 0
                # datas["3_5"] += 1 if result.home_score + result.away_score < 3.5 else 0
                
                # home_rank = LigneRanking.objects.filter(team = match.home, ranking__date__lte = match.date).order_by('-ranking__date').first()
                # away_rank = LigneRanking.objects.filter(team = match.away, ranking__date__lte = match.date).order_by('-ranking__date').first()
                
                moy += (result.home_score + result.away_score) / len(matchs)
            
            if (moy >= 2.7):
                for x in [1.5, 2.5, 3.5]:
                    p = fish_law_plus(moy, x)
                    if p >= 85:
                        Prediction.objects.create(
                            mode = ModePrediction.get("M4"),
                            type = TypePrediction.get("p{}".format(str(x).replace(".", "_"))),
                            match = match,
                            pct = p
                        )
                    
                    
            if (moy <= 2):
                for x in [1.5, 2.5, 3.5]:
                    p = fish_law_moins(moy, x)
                    if p >= 85:
                        Prediction.objects.create(
                            mode = ModePrediction.get("M4"),
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
                    mode = ModePrediction.get("M4"),
                    type = TypePrediction.get("VN_{}".format("Home" if ppg_home >= ppg_away else "Away" )),
                    match = match,
                    pct = p
                )
                
        