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
import numpy as np
from scipy.stats import poisson, skellam



class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

        

    def handle(self, *args, **options):
        PredictionScore.objects.all().delete()
        PredictionTest.objects.all().delete()
        for match in Match.objects.filter(is_finished = True).order_by('-date')[:5000]:
            if len( match.away.get_last_matchs(match, edition = True)) < 4 or len( match.home.get_last_matchs(match, edition = True)) < 4:
                continue
            
            home_stats = match.get_home_before_stats()
            away_stats = match.get_away_before_stats()
            min_points = min(home_stats.points, away_stats.points)
            

            pts, ppg, scored, avg_goals_scored_h, conceded, avg_goals_conceded_h = match.home.last_stats(match, edition = True, number = 10)
            pts, ppg, scored, avg_goals_scored_a, conceded, avg_goals_conceded_a = match.away.last_stats(match, edition = True, number = 10)
            
            avg1 = moyenne_but(avg_goals_scored_h, avg_goals_conceded_a)
            datas1 = {}
            for x in [0, 1, 2, 3, 4, 5]:
                datas1[x] = round(fish_law(avg1, x) / 100, 2)
            
            
            avg2 = moyenne_but(avg_goals_scored_a, avg_goals_conceded_h )
            datas2 = {}
            for x in [0, 1, 2, 3, 4, 5]:
                datas2[x] = round(fish_law(avg2, x) / 100, 2)


            datas = {}
            for x in datas1:
                for y in datas2:
                    taux = datas1[x] * datas2[y] * 100
                    if taux >= 10:
                        datas[(x, y)] = round(taux, 2)
            datas = sorted(datas.items(), key = lambda x:-x[1])


            if len(datas) == 0:
                continue
            
            
            # if len(datas) == 1:
            #     score = datas[0][0]
            #     if score[0] == 1 and score[1] == 1:
            #         PredictionTest.objects.create(
            #             mode = ModePrediction.get("M0"),
            #             type = TypePrediction.get("12"),
            #             match = match,
            #             pct = 85
            #         )
            #         PredictionTest.objects.create(
            #             mode = ModePrediction.get("M0"),
            #             type = TypePrediction.get("m3_5"),
            #             match = match,
            #             pct = 85
            #         )
            
            #     elif score[0] - score[1] >= 2:
            #         PredictionTest.objects.create(
            #             mode = ModePrediction.get("M0"),
            #             type = TypePrediction.get("1X"),
            #             match = match,
            #             pct = 85
            #         )
            #         PredictionTest.objects.create(
            #             mode = ModePrediction.get("M0"),
            #             type = TypePrediction.get("But_Home"),
            #             match = match,
            #             pct = 85
            #         )
                    
            #     elif score[1] - score[0] >= 2:
            #         PredictionTest.objects.create(
            #             mode = ModePrediction.get("M0"),
            #             type = TypePrediction.get("X2"),
            #             match = match,
            #             pct = 85
            #         )
            #         PredictionTest.objects.create(
            #             mode = ModePrediction.get("M0"),
            #             type = TypePrediction.get("But_Away"),
            #             match = match,
            #             pct = 85
            #         )
                    
            # continue

            
            # score_proba = np.zeros((5, 5))
            # for i in range(5):
            #     for j in range(5):
            #         score_proba[i, j] = poisson.pmf(i, avg_goals_scored_h) * poisson.pmf(j, avg_goals_scored_a)

            # # Obtenir les scores dont la probabilité est supérieure à 0.01 et les trier par ordre décroissant de probabilité
            # scores = [(i, j, score_proba[i, j]) for i in range(5) for j in range(5) if score_proba[i, j] > 0.01]
            # scores_sorted = sorted(scores, key=lambda x: x[2], reverse=True)

            # # Calculer la probabilité d'avoir un écart de buts donné
            # skellam_proba = skellam.pmf(np.arange(-5, 6), avg_goals_scored_h, avg_goals_scored_a)
            # home_win_proba = np.sum(skellam_proba[6:])
            # away_win_proba = np.sum(skellam_proba[:5])
            # draw_proba = skellam_proba[5]
            
            


        
            ho = aw = 0
            for i, x in enumerate(datas):
                if x[1] > 10 :
                    ho += x[0][0]
                    aw += x[0][1] 
            if len(datas) > 2:
                if (ho > aw or avg1 > 2.5*avg2)  and home_stats.points - 10 >= away_stats.points*1.5:
                    PredictionTest.objects.create(
                        mode = ModePrediction.get("M0"),
                        type = TypePrediction.get("1X"),
                        match = match,
                        pct = 85
                    )
                elif ((aw >=2 and  ho == 0) or avg2 > 2.5*avg1 )and home_stats.points*1.5 <= away_stats.points:
                    PredictionTest.objects.create(
                        mode = ModePrediction.get("M0"),
                        type = TypePrediction.get("X2"),
                        match = match,
                        pct = 85
                    )
                # elif ho > 2 and abs(ho -aw) > 2 and home_stats.points + away_stats.points >= min_points * 3:
                #     pass
                    # PredictionTest.objects.create(
                    #     mode = ModePrediction.get("M0"),
                    #     type = TypePrediction.get("p1_5"),
                    #     match = match,
                    #     pct = 85
                    # )
                        
                        
                # if ho >= 3:
                #     PredictionTest.objects.create(
                #         mode = ModePrediction.get("M0"),
                #         type = TypePrediction.get("But_Home"),
                #         match = match,
                #         pct = 85
                #     )
                # elif aw >= 3 and away_stats.points > min_points :
                #     PredictionTest.objects.create(
                #         mode = ModePrediction.get("M0"),
                #         type = TypePrediction.get("But_Away"),
                #         match = match,
                #         pct = 85
                #     )
                    
            else:
                pass
                
                # if abs(ho -aw) <= 1 and abs(home_stats.points - away_stats.points) < min_points:
                #     for i, x in enumerate(datas):
                #         if x[0][0] == x[0][1] :
                #             PredictionTest.objects.create(
                #                 mode = ModePrediction.get("M0"),
                #                 type = TypePrediction.get("12"),
                #                 match = match,
                #                 pct = 85
                #             )
                #             break
                        
                # if home_stats.points + away_stats.points >= min_points * 3:
                #     PredictionTest.objects.create(
                #         mode = ModePrediction.get("M0"),
                #         type = TypePrediction.get("p1_5"),
                #         match = match,
                #         pct = 85
                #     )
                    
                # if len(datas) == 2 and (ho - aw >= 2 or avg1 > 2*avg2) :
                #     PredictionTest.objects.create(
                #         mode = ModePrediction.get("M0"),
                #         type = TypePrediction.get("1X"),
                #         match = match,
                #         pct = 85
                #     )
                    
                # if len(datas) == 2 and (aw - ho > 2 or avg2 > 2*avg1) :
                #     PredictionTest.objects.create(
                #         mode = ModePrediction.get("M0"),
                #         type = TypePrediction.get("X2"),
                #         match = match,
                #         pct = 85
                #     )
                    
                
            # t = 0
            # for i, x in enumerate(datas):
            #     if (x[0][0] in [0, 1] and x[0][1] in [0, 1]) and not (x[0][0] == x[0][1] == 1) and i < 4:
            #         t += x[1]   
            # if t > 60 and abs(home_stats.points - away_stats.points) <= min_points :
            #     PredictionTest.objects.create(
            #         mode = ModePrediction.get("M0"),
            #         type = TypePrediction.get("m3_5"),
            #         match = match,
            #         pct = t
            #     )
                

            
            
            
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
            # if home_stats.avg_corners_for == 0 and away_stats.avg_corners_against == 0:
            #     continue
                
            # print(match, match.date)
            # avg1 = (home_stats.avg_corners_for + away_stats.avg_corners_against) /2
            # # datas1 = {}
            # for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            #     t = fish_law(avg, x)
            #     if t >= 0.15:
            #         datas1[x] = round(t / 100, 2)
            # print(datas1)
            
            
            # avg2 = (away_stats.avg_corners_for + home_stats.avg_corners_against ) / 2
            # datas2 = {}
            # for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            #     t = fish_law(avg, x)
            #     if t >= 0.15:
            #         datas2[x] = round(t / 100, 2)
            # print(datas2)
            
            print('--------------------', avg1, avg2)
            # datas = {}
            # for x in datas1:
            #     for y in datas2:
            #         taux = datas1[x] * datas2[y] * 100
            #         if taux >= 10:
            #             datas[(x, y)] = round(taux, 2)
            # datas = sorted(datas.items(), key = lambda x:-x[1])

            
            # for i, x in enumerate(datas):
            #     if x[1] > 10 and i < 4:
            #         print(x, x[0][0], x[0][1])
                    # PredictionScore.objects.create(
                    #     home_score = x[0][0],
                    #     away_score = x[0][1],
                    #     match = match,
                    #     pct = x[1]
                    # )
                    

            # if avg1 + avg2 >= 10 and home_stats.avg_corners_for >= 6 and  away_stats.avg_corners_for >= 6 and abs(home_stats.points - away_stats.points) > min_points*2:
            #     PredictionTest.objects.create(
            #         mode = ModePrediction.get("M0"),
            #         type = TypePrediction.get("corner_p7_5"),
            #         match = match,
            #         pct = 85
            #     )
                
                
            # if avg1 + avg2 < 9 and home_stats.avg_corners_for < 5:
            #     PredictionTest.objects.create(
            #         mode = ModePrediction.get("M0"),
            #         type = TypePrediction.get("corner_m12_5"),
            #         match = match,
            #         pct = 85
            #     )
                        
     
                    
            break
            print("-------------------------------------------------------------------")
            extra = match.get_extra_info_match()
            
            competitionstats = match.edition.edition_stats.filter(ranking__date__lte = match.date).order_by('-created_at').first()
            home_stats = match.get_home_before_stats()
            away_stats = match.get_away_before_stats()
            
            if home_stats is not None and away_stats is not None: 
                pre = ((home_stats.avg_corners_for or 0) + (home_stats.avg_corners_against or 0) + (away_stats.avg_corners_for or 0) + (away_stats.avg_corners_against or 0)) / 2
                # out = (extra.home_corners or 0 )+ (extra.away_corners or 0)
                # if not out == 0:
                    
                if 0 < pre >= 14:
                    if home_stats.avg_corners_for + away_stats.avg_corners_against >= competitionstats.avg_corners and  home_stats.avg_corners_against + away_stats.avg_corners_for >= competitionstats.avg_corners:
                        PredictionTest.objects.create(
                            mode = ModePrediction.get("M0"),
                            type = TypePrediction.get("corner_p7_5"),
                            match = match,
                            pct = 85
                        )
                    
                    print("--------------------------", match, pre)
                    if 0 < pre < 9:
                        if home_stats.avg_corners_for < 10 and home_stats.avg_corners_against < 10 and  away_stats.avg_corners_for < 10 and away_stats.avg_corners_against < 10 :
                            Prediction.objects.create(
                                mode = ModePrediction.get("M0"),
                                type = TypePrediction.get("corner_m12_5"),
                                match = match,
                                pct = 85
                            )
                            
            
            
            # score_proba = np.zeros((10, 10))
            # for i in range(10):
            #     for j in range(10):
            #         score_proba[i, j] = poisson.pmf(i, avg_goals_scored_h) * poisson.pmf(j, avg_goals_scored_a)

            # # Obtenir les scores dont la probabilité est supérieure à 0.01 et les trier par ordre décroissant de probabilité
            # scores = [(i, j, score_proba[i, j]) for i in range(10) for j in range(10) if score_proba[i, j] > 0.01]
            # scores_sorted = sorted(scores, key=lambda x: x[2], reverse=True)

            # # Calculer la probabilité d'avoir un écart de buts donné
            # skellam_proba = skellam.pmf(np.arange(-10, 11), avg_goals_scored_h, avg_goals_scored_a)
            # # home_win_proba = np.sum(skellam_proba[11:])
            # # away_win_proba = np.sum(skellam_proba[:10])
            # # draw_proba = skellam_proba[10]

            # # # Afficher les résultats en pourcentage
            # # print(f"Probabilité de victoire à domicile : {home_win_proba*100:.2f}%")
            # # print(f"Probabilité de match nul : {draw_proba*100:.2f}%")
            # # print(f"Probabilité de victoire à l'extérieur : {away_win_proba*100:.2f}%")

            # # Afficher les scores avec leur probabilité
            # print("Scores les plus probables :")
            # for score in scores_sorted:
            #     if score[2] > 0.1:
            #         for i, proba in enumerate(skellam_proba):
            #             if proba > 0.05 and i-10 == score[0]-score[1]:
            #                 print(f"{score[0]}-{score[1]} : {score[2]*100:.2f}% avec {i-10}: {proba:.2%}")
            #                 PredictionScore.objects.create(
            #                     home_score = score[0],
            #                     away_score = score[1],
            #                     match = match,
            #                     pct = score[2]
            #                 )
            #                 break
