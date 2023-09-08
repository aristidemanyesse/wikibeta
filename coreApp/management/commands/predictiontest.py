from django.core.management.base import BaseCommand, CommandError
import predictionApp.functions.p0 as p0
import predictionApp.functions.p1 as p1
import predictionApp.functions.p2 as p2
import predictionApp.functions.p3 as p3
import predictionApp.functions.p4 as p4
from competitionApp.models import *
from predictionApp.models import *
from coreApp.templatetags import footstats
# from tensorflow import keras

import statsApp.get_home_facts as get_home_facts
import statsApp.get_away_facts as get_away_facts
import math
import threading
import os, time
import numpy as np
from scipy.stats import poisson, skellam


def predict(match):
    try:
        home_last_matchs = match.home.get_last_matchs(match, number = 10, edition = True)
        away_last_matchs = match.away.get_last_matchs(match, number = 10, edition = True)
                
        if not (len(home_last_matchs) > 3 and len(away_last_matchs) > 3):
            match.is_predict = True
            match.save()
            
        home_stats = match.get_home_before_stats()
        away_stats = match.get_away_before_stats()
        
        home_rank = LigneRanking.objects.filter(team = match.home, ranking__date__lte = match.date).order_by('-ranking__date').first()
        away_rank = LigneRanking.objects.filter(team = match.away, ranking__date__lte = match.date).order_by('-ranking__date').first()

        
        if home_stats is not None and away_stats is not None:
            
            # if (home_stats.score_elo >= 1600 and away_stats.score_elo >= 1600):
            #     PredictionTest.objects.create(
            #         mode = ModePrediction.get("M0"),
            #         type = TypePrediction.get("p1_5"),
            #         match = match,
            #         pct = 0.80
            #     )
                
            if (home_stats.ga_expected < 0.7 and away_stats.ga_expected < 0.7):
                PredictionTest.objects.create(
                    mode = ModePrediction.get("M0"),
                    type = TypePrediction.get("m3_5"),
                    match = match,
                    pct = 0.80
                )
                
            if (home_stats.ga_expected > 0.7 and away_stats.ga_expected > 0.7):
                PredictionTest.objects.create(
                    mode = ModePrediction.get("M0"),
                    type = TypePrediction.get("p1_5"),
                    match = match,
                    pct = 0.80
                )
                
            # if (home_stats.probabilite_elo > 0.6):
            #     PredictionTest.objects.create(
            #         mode = ModePrediction.get("M0"),
            #         type = TypePrediction.get("1X"),
            #         match = match,
            #         pct = 0.80
            #     )
                
            # elif (away_stats.probabilite_elo > 0.60):
            #     PredictionTest.objects.create(
            #         mode = ModePrediction.get("M0"),
            #         type = TypePrediction.get("p1_5"),
            #         match = match,
            #         pct = 0.80
            #     )
                
                
            # if  1 <= home_stats.ppg < 2 and 1 <= away_stats.ppg < 2:
            #     PredictionTest.objects.create(
            #         mode = ModePrediction.get("M0"),
            #         type = TypePrediction.get("12"),
            #         match = match,
            #         pct = 0.80
            #     )
                
            if  home_stats.ppg >= 2 and away_stats.ppg >= 2:
                if ((home_rank.avg_ga + away_rank.avg_ga) >= 2.5):
                    pass
                    # PredictionTest.objects.create(
                    #     mode = ModePrediction.get("M0"),
                    #     type = TypePrediction.get("p1_5"),
                    #     match = match,
                    #     pct = 0.80
                    # )
                else:
                    if 0.40 < home_stats.probabilite_elo < 0.6:
                        pass
                        # PredictionTest.objects.create(
                        #     mode = ModePrediction.get("M0"),
                        #     type = TypePrediction.get("m3_5"),
                        #     match = match,
                        #     pct = 0.80
                        # )
                
            # if len(home_last_matchs) >= 8 and len(away_last_matchs) >= 8:
            #     if 0.49 < home_stats.probabilite_elo < 0.51:
            #         PredictionTest.objects.create(
            #             mode = ModePrediction.get("M0"),
            #             type = TypePrediction.get("12"),
            #             match = match,
            #             pct = 0.80
            #         )
            #         PredictionTest.objects.create(
            #             mode = ModePrediction.get("M0"),
            #             type = TypePrediction.get("m3_5"),
            #             match = match,
            #             pct = 0.80
            #         )
            
            # home_rank = LigneRanking.objects.filter(team = match.home, ranking__date__lte = match.date).order_by('-ranking__date').first()
            # away_rank = LigneRanking.objects.filter(team = match.away, ranking__date__lte = match.date).order_by('-ranking__date').first()

            # p = footstats.plus_but(home_last_matchs, 2.5) + footstats.plus_but(away_last_matchs, 2.5)
            # m = footstats.moins_but(home_last_matchs, 2.5) + footstats.moins_but(away_last_matchs, 2.5)
            # # p4 = footstats.plus_but(home_last_matchs, 3.5) + footstats.plus_but(away_last_matchs, 3.5)
            
            # if p + m  >= 10 :
            #     # ############################################################################################################################
            #     # # PLUS DE 1.5 BUTS DANS LE MATCH
            #     # ############################################################################################################################
            #     # a, b = match.edition.plus_but(1.5)
            #     # ratio = a / b
                
            #     # if (p > m+1) and (home_rank.avg_gs + away_rank.avg_gs) >= 2.3 and ratio > 0.55:
            #     #     PredictionTest.objects.create(
            #     #         mode = ModePrediction.get("M0"),
            #     #         type = TypePrediction.get("p1_5"),
            #     #         match = match,
            #     #         pct = round((p / 20 ), 2) * 100
            #     #     )
            
            
            #     ############################################################################################################################
            #     # MOINS DE 3.5 BUTS DANS LE MATCH
            #     ############################################################################################################################
            #     a, b = match.edition.moins_but(3.5)
            #     ratio = a / b
                
            #     if (m >= p+1)  and (home_rank.avg_gs + away_rank.avg_gs) < 2.5 and ratio > 0.55: #and (home_rank.avg_ga + away_rank.avg_ga) <= 2.5  and (home_rank.avg_gs + away_rank.avg_gs) < 2.5
            #         PredictionTest.objects.create(
            #             mode = ModePrediction.get("M0"),
            #             type = TypePrediction.get("m3_5"),
            #             match = match,
            #             pct = round((p / 20 ), 2) * 100
            #         )
            
        
    except Exception as e:
        print("prediction test error:", e)



class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            PredictionTest.objects.all().delete()            
            for match in Match.objects.filter(is_compared = True).exclude(is_predict = True).order_by('date')[:1000]:
                print("START: Current active thread count ---------------: ", threading.active_count())
                while threading.active_count() > 300:
                    time.sleep(10)
                    
                p = threading.Thread(target=predict, args=(match,))
                p.setDaemon(True)
                p.start()
                time.sleep(0.1)
                
                # p = threading.Thread(target=p1.predict, args=(match,))
                # p.setDaemon(True)
                # p.start()
                # time.sleep(0.01)
                
                # p = threading.Thread(target=p2.predict, args=(match,))
                # p.setDaemon(True)
                # p.start()
                # time.sleep(0.01)
                
                # p = threading.Thread(target=p3.predict, args=(match,))
                # p.setDaemon(True)
                # p.start()
                # time.sleep(0.01)

                # p = threading.Thread(target=p4.predict, args=(match,))
                # p.setDaemon(True)
                # p.start()
                # time.sleep(0.01)
                
                # match.is_predict = True
                # match.save()
                
                print(match)
                    
            while threading.active_count() > 1:
                print("en attente ---------------: ", threading.active_count())
                time.sleep(25)
            self.stdout.write(self.style.SUCCESS('List des matchs facted avec succes !'))    
                
        except Exception as e:
            print(e)
            
     

