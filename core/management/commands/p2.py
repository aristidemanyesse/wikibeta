from django.core.management.base import BaseCommand, CommandError
from prediction.models import *
from features.models import *
from dateparser import parse

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for match in Match.objects.all():
            matchs = match.similaires_ppg()
            if len(matchs) >= 3 :
                moy = 0
                for x in matchs:
                    moy += (x.home_score + x.away_score) / len(matchs)
                if (not(1.8 < moy < 3)):
                    p = fish_law_plus(moy, 1.5)
                    if p >= 85:
                        Prediction.objects.create(
                            mode = ModePrediction.get("M2"),
                            type = TypePrediction.get("p1_5"),
                            match = match,
                            pct = p
                        )
                        
                    p = fish_law_plus(moy, 2.5)
                    if p >= 85:
                        Prediction.objects.create(
                            mode = ModePrediction.get("M2"),
                            type = TypePrediction.get("p2_5"),
                            match = match,
                            pct = p
                        )
                        
                        
                    p = fish_law_moins(moy, 2.5)
                    if p >= 85:
                        Prediction.objects.create(
                            mode = ModePrediction.get("M2"),
                            type = TypePrediction.get("m2_5"),
                            match = match,
                            pct = p
                        )
                        
                    p = fish_law_moins(moy, 3.5)
                    if p >= 85:
                        Prediction.objects.create(
                            mode = ModePrediction.get("M2"),
                            type = TypePrediction.get("m3_5"),
                            match = match,
                            pct = p
                        )

            
            
        
        matchs = match.similaires_ppg()
        for x in matchs:
            print(x, x.score())
            
        if len(matchs) > 0:
            moy = 0
            for x in matchs:
                moy += (x.home_score + x.away_score) / len(matchs)
        
            print(moy)
            print("1.5  ===>", fish_law_plus(moy, 1.5))
            print("2.5  ===>", fish_law_plus(moy, 2.5))
            print("3.5  ===>", fish_law_plus(moy, 3.5))
            print("-2.5  ===>", fish_law_moins(moy, 2.5))
            print("-3.5  ===>", fish_law_moins(moy, 3.5))
            print("-4.5  ===>", fish_law_moins(moy, 4.5))