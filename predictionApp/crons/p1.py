from prediction.models import *
from fixtureApp.models import *

def function(self, *args, **options):
    for match in Match.objects.filter(is_finished = False).order_by("-date"):
        print("Prédiction pour {}".format(match))
        matchs = match.confrontations_directes()
        if len(matchs) >= 14 :
            moy = 0
            for x in matchs:
                moy += (x.home_score + x.away_score) / len(matchs)
                
                
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