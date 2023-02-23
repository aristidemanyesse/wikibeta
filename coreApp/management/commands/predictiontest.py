from django.core.management.base import BaseCommand, CommandError
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
    
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

        

    def handle(self, *args, **options):
        # PredictionScore.objects.all().delete()
        # for match in Match.objects.filter().order_by('-date')[:3000]:
        #     print(match, match.date)
            
        #     pts, ppg, scored, avg_goals_scored, conceded, avg_goals_conceded = match.home.last_stats(match, edition = True, number = 10)
        #     avg = moyenne_but(avg_goals_scored, avg_goals_conceded)
        #     datas1 = {}
        #     for x in [0, 1, 2, 3, 4, 5]:
        #         datas1[x] = round(fish_law(avg, x) / 100, 2)
            
            
        #     pts, ppg, scored, avg_goals_scored, conceded, avg_goals_conceded = match.away.last_stats(match, edition = True, number = 10)
        #     avg = moyenne_but(avg_goals_scored, avg_goals_conceded )
        #     datas2 = {}
        #     for x in [0, 1, 2, 3, 4, 5]:
        #         datas2[x] = round(fish_law(avg, x) / 100, 2)


        #     datas = {}
        #     for x in datas1:
        #         for y in datas2:
        #             datas[(x, y)] = round(datas1[x] * datas2[y] * 100, 2)
        #     datas = sorted(datas.items(), key = lambda x:-x[1])
            
        #     for i, x in enumerate(datas):
        #         if x[1] > 10 and i < 4:
        #             print(x, x[0][0], x[0][1])
        #             PredictionScore.objects.create(
        #                 home_score = x[0][0],
        #                 away_score = x[0][1],
        #                 match = match,
        #                 pct = x[1]
        #             )
                    
                    
        def in_score(table, tuple):
            for x in table:
                if x.home_score == tuple[0] and x.away_score == tuple[1]:
                    return True
            return False

        
        PredictionTest.objects.all().delete()
        for match in Match.objects.filter().order_by('-date')[:3000]:   
            scores = match.predictionscore_match.filter()
            print("--------------------", match, match.date)
            
            if len(scores) == 4 and in_score(scores, (0, 0)) and in_score(scores, (0, 1)) and in_score(scores, (1, 0)) and in_score(scores, (1, 1)) :
                PredictionTest.objects.create(
                    mode = ModePrediction.get("M0"),
                    type = TypePrediction.get("m3_5"),
                    match = match,
                    pct = 80
                )
                    
                    
            if 0 < len(scores) < 3:
                if in_score(scores, (1, 1)) or in_score(scores, (0, 0)):
                    PredictionTest.objects.create(
                        mode = ModePrediction.get("M0"),
                        type = TypePrediction.get("12"),
                        match = match,
                        pct = 80
                    )
                    
                    
                    
                    
                    
                    
                    
            #         print(x[0] , "******", x[1])
            # break
            print("-------------------------------------------------------------------")
            # extra = match.get_extra_info_match()
            
            # competitionstats = match.edition.edition_stats.filter(ranking__date__lte = match.date).order_by('-created_at').first()

            
            # if home_stats is not None and away_stats is not None: 
            #     pre = ((home_stats.avg_corners_for or 0) + (home_stats.avg_corners_against or 0) + (away_stats.avg_corners_for or 0) + (away_stats.avg_corners_against or 0)) / 2
            #     # out = (extra.home_corners or 0 )+ (extra.away_corners or 0)
            #     # if not out == 0:
                    
            #     if 0 < pre >= 14:
            #         if home_stats.avg_corners_for + away_stats.avg_corners_against >= competitionstats.avg_corners and  home_stats.avg_corners_against + away_stats.avg_corners_for >= competitionstats.avg_corners:
            #             PredictionTest.objects.create(
            #                 mode = ModePrediction.get("M0"),
            #                 type = TypePrediction.get("corner_p8_5"),
            #                 match = match,
            #                 pct = 95
            #             )
                    
                    # print("--------------------------", match, pre)
                    # if 0 < pre < 9:
                    #     if home_stats.avg_corners_for < 10 and home_stats.avg_corners_against < 10 and  away_stats.avg_corners_for < 10 and away_stats.avg_corners_against < 10 :
                    #         Prediction.objects.create(
                    #             mode = ModePrediction.get("M0"),
                    #             type = TypePrediction.get("corner_m12_5"),
                    #             match = match,
                    #             pct = 95
                    #         )
                            
                    