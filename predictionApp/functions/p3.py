from predictionApp.models import *
from fixtureApp.models import *


def function(edition):
    for match in edition.edition_du_match.all():
        if match.prediction_match.all().count() == 0 :
            predict(match)
    
    
def predict(match):
    scores = match.predictionscore_match.filter()
    list_scores = []
    for score in scores :
        list_scores.append("{}:{}".format(score.home_score, score.away_score))
    print(list_scores)
    if list_scores in ["0:0", "0:1", "1:0", "1:1"]:
        PredictionTest.objects.create(
            mode = ModePrediction.get("M3"),
            type = TypePrediction.get("m3_5"),
            match = match,
            pct = 0.8
        )
    
    test = True
    for score in scores :
        if not (score.home_score > 0 and score.away_score > 0):
            test = False
            break
    if test:
        PredictionTest.objects.create(
            mode = ModePrediction.get("M3"),
            type = TypePrediction.get("btts"),
            match = match,
            pct = 0.8
        )
    
    test = True
    total = 0
    for score in scores :
        total += score.home_score + score.away_score
        if not (score.home_score + score.away_score > 1.5):
            test = False
            break
    if test or total >= 6:
        PredictionTest.objects.create(
            mode = ModePrediction.get("M3"),
            type = TypePrediction.get("p1_5"),
            match = match,
            pct = 0.8
        )
    
    test = True
    for score in scores :
        if not (score.home_score > 0):
            test = False
            break
    if test:
        PredictionTest.objects.create(
            mode = ModePrediction.get("M3"),
            type = TypePrediction.get("HG"),
            match = match,
            pct = 0.8
        )
    
                
    
    test = True
    for score in scores :
        if not (score.away_score > 0):
            test = False
            break
    if test:
        PredictionTest.objects.create(
            mode = ModePrediction.get("M3"),
            type = TypePrediction.get("AG"),
            match = match,
            pct = 0.8
        )
    
                
                