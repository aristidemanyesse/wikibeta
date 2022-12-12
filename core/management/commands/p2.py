from django.core.management.base import BaseCommand, CommandError
from prediction.models import *
from features.models import *
from dateparser import parse

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for match in Match.objects.all():
            print("Prédiction pour {}".format(match))
            matchs = match.similaires_ppg()
            if len(matchs) >= 14 :
                moy = 0
                for x in matchs:
                    moy += (x.home_score + x.away_score) / len(matchs)
                    
                if (moy >= 2.7):
                    for x in [1.5, 2.5, 3.5]:
                        p = fish_law_plus(moy, x)
                        if p >= 85:
                            Prediction.objects.create(
                                mode = ModePrediction.get("M2"),
                                type = TypePrediction.get("p{}".format(str(x).replace(".", "_"))),
                                match = match,
                                pct = p
                            )
                        
                        
                if (moy <= 2):
                    for x in [1.5, 2.5, 3.5]:
                        p = fish_law_moins(moy, x)
                        if p >= 85:
                            Prediction.objects.create(
                                mode = ModePrediction.get("M2"),
                                type = TypePrediction.get("m{}".format(str(x).replace(".", "_"))),
                                match = match,
                                pct = p
                            )
                continue
                total = 0     
                for x in matchs:
                    ppg_home = x.get_home_before_stats().ppg
                    ppg_away = x.get_away_before_stats().ppg
                    
                    if ppg_home == ppg_away :
                        total += 1
                    elif ppg_home > ppg_away and x.home_score >= x.away_score :
                        total += 1
                    elif ppg_home < ppg_away and x.home_score <= x.away_score :
                        total += 1
                
                p = (total / len(matchs)) * 100
                if p >= 90:
                    Prediction.objects.create(
                        mode = ModePrediction.get("M2"),
                        type = TypePrediction.get("VN_{}".format("Home" if ppg_home >= ppg_away else "Away" )),
                        match = match,
                        pct = p
                    )
                elif p <= 10:
                    Prediction.objects.create(
                        mode = ModePrediction.get("M2"),
                        type = TypePrediction.get("VN_{}".format("Away" if ppg_home >= ppg_away else "Home" )),
                        match = match,
                        pct = 100 - p
                    )