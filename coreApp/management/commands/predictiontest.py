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
        if len( match.away.get_last_matchs(match, edition = True)) >= 3 and len( match.home.get_last_matchs(match, edition = True)) >= 3:
            
            home_stats = match.get_home_before_stats()
            away_stats = match.get_away_before_stats()
            
            if home_stats is not None and away_stats is not None:
                home_last_matchs = match.home.get_last_matchs(match, number = 10, edition = True)
                away_last_matchs = match.away.get_last_matchs(match, number = 10, edition = True)
                
                home_rank = LigneRanking.objects.filter(team = match.home, ranking__date__lte = match.date).order_by('-ranking__date').first()
                away_rank = LigneRanking.objects.filter(team = match.away, ranking__date__lte = match.date).order_by('-ranking__date').first()

                p = footstats.plus_but(home_last_matchs, 2.5) + footstats.plus_but(away_last_matchs, 2.5)
                m = footstats.moins_but(home_last_matchs, 2.5) + footstats.moins_but(away_last_matchs, 2.5)
                # p4 = footstats.plus_but(home_last_matchs, 3.5) + footstats.plus_but(away_last_matchs, 3.5)
                
                if p + m  >= 10 :
                    # ############################################################################################################################
                    # # PLUS DE 1.5 BUTS DANS LE MATCH
                    # ############################################################################################################################
                    # a, b = match.edition.plus_but(1.5)
                    # ratio = a / b
                    
                    # if (p > m+1) and (home_rank.avg_gs + away_rank.avg_gs) >= 2.3 and ratio > 0.55:
                    #     PredictionTest.objects.create(
                    #         mode = ModePrediction.get("M0"),
                    #         type = TypePrediction.get("p1_5"),
                    #         match = match,
                    #         pct = round((p / 20 ), 2) * 100
                    #     )
                
                
                    ############################################################################################################################
                    # MOINS DE 3.5 BUTS DANS LE MATCH
                    ############################################################################################################################
                    a, b = match.edition.moins_but(3.5)
                    ratio = a / b
                    
                    if (m >= p+1)  and (home_rank.avg_gs + away_rank.avg_gs) < 2.5 and ratio > 0.55: #and (home_rank.avg_ga + away_rank.avg_ga) <= 2.5  and (home_rank.avg_gs + away_rank.avg_gs) < 2.5
                        PredictionTest.objects.create(
                            mode = ModePrediction.get("M0"),
                            type = TypePrediction.get("m3_5"),
                            match = match,
                            pct = round((p / 20 ), 2) * 100
                        )
                
        
    except Exception as e:
        print("prediction test error:", e)



class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            PredictionTest.objects.all().delete()            
            for match in Match.objects.filter(is_facted = True).exclude(is_predict = True).order_by('date')[:1000]:
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
            
     

