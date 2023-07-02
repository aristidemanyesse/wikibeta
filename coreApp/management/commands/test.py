import numpy as np
import pandas as pd
import math
from django.db.models import Avg
from django.core.management.base import BaseCommand
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from fixtureApp.models import Match

import predictionApp.functions.p0 as p0
import predictionApp.functions.p1 as p1
import predictionApp.functions.p2 as p2
import predictionApp.functions.p3 as p3
import predictionApp.functions.p4 as p4
from competitionApp.models import *
from predictionApp.models import *

import statsApp.get_home_facts as get_home_facts
import statsApp.get_away_facts as get_away_facts
import math
import threading
import os, time
import numpy as np
from scipy.stats import poisson, skellam



class Command(BaseCommand):
    help = 'Train neural network to predict goals in football matches'

    def handle(self, *args, **options):
        # Load data from Django models
        matches = Match.objects.filter(is_finished = True).order_by('-date')[:5000]

        # Preprocess data
        data = []
        for match in matches:
            result = match.get_result()
if result is None:
                test += 1
                continue
            odds = match.get_odds()
            pts_h, ppg_h, scored, avg_goals_scored_h, conceded, avg_goals_conceded_h = match.home.last_stats(match, edition = True, number = 10)
            pts_a, ppg_a, scored, avg_goals_scored_a, conceded, avg_goals_conceded_a = match.away.last_stats(match, edition = True, number = 10)
            
            p1_5 = result.home_score + result.away_score > 1.5
            m3_5 = result.home_score + result.away_score < 3.5
            btts = result.home_score > 0 and  result.away_score > 0
            
            data.append([avg_goals_scored_h, avg_goals_conceded_h, ppg_h, pts_h,  avg_goals_scored_a, avg_goals_conceded_a, ppg_a, pts_a, odds.home, odds.draw, odds.away, result.home_score, result.away_score, result.home_score + result.away_score, p1_5, m3_5, btts ])

        with open("./data.json", "w") as file:
            file.write(json.dumps(data))
    
    
    
# def main(match):
#     print("--------------------------------", match, match.edition)
#     confrontations        = json.dumps([str(x.id) for x in match.confrontations_directes(10)])
#     similaires_ppg        = json.dumps([str(x.id) for x in match.similaires_ppg(10)])
#     similaires_ppg2       = json.dumps([str(x.id) for x in match.similaires_ppg2(10)])
#     similaires_betting    = json.dumps([str(x.id) for x in match.similaires_betting(10)])
    
#     for stats in [match.get_home_before_stats(), match.get_away_before_stats()]:
#         stats.list_confrontations         = confrontations
#         stats.list_similaires_ppg         = similaires_ppg
#         stats.list_similaires_ppg2        = similaires_ppg2
#         stats.list_similaires_betting     = similaires_betting
#         stats.save()


# class Command(BaseCommand):


#     def handle(self, *args, **options):
#         print(BeforeMatchStat.objects.filter(points = None).order_by("-match__date").count())
#         # for match in Match.objects.filter(date__lte = datetime.datetime.now() - datetime.timedelta(days=3)).order_by('-date'):
#         #     while threading.active_count() >= 800:
#         #         print("processus en cours ---------------: ", threading.active_count())
#         #         time.sleep(5)
#         #     p = threading.Thread(target=main , args=(match,))
#         #     p.setDaemon(True)
#         #     p.start()
#         #     time.sleep(1)
            
#         # while threading.active_count() > 0:
#         #     print("en attente ---------------: ", threading.active_count())
#         #     time.sleep(30)
#         # self.stdout.write(self.style.SUCCESS('List des matchs initialisée avec succes !'))  
                                
            



