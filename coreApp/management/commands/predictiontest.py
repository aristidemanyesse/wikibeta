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



class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

        

    def handle(self, *args, **options):
        # PredictionScore.objects.all().delete()
        PredictionTest.objects.all().delete()
        

        matchs = Match.objects.filter(is_finished = False).exclude(is_posted = True).order_by('?')[:20000]
        
        for nb, match in enumerate(matchs):
            if len( match.away.get_last_matchs(match, edition = True)) < 4 or len( match.home.get_last_matchs(match, edition = True)) < 4:
                continue
            
            print(nb, match, match.date)
            
            competitionstats = match.edition.edition_stats.filter(ranking__date__lte = match.date).order_by('-created_at').first()
            home_last_matchs = match.home.get_last_matchs(match, number = 10, edition = True)
            away_last_matchs = match.away.get_last_matchs(match, number = 10, edition = True)
            
            # pts_h, ppg, scored, avg_goals_scored_h, conceded, avg_goals_conceded_h = match.home.last_stats(match, edition = True, number = 5)
            # pts_a, ppg, scored, avg_goals_scored_a, conceded, avg_goals_conceded_a = match.away.last_stats(match, edition = True, number = 5)
            
            # home_facts = match.match_facts.filter(team = match.home)
            # away_facts = match.match_facts.filter(team = match.away)
            
            home_rank = LigneRanking.objects.filter(team = match.home, ranking__date__lte = match.date).order_by('-ranking__date').first()
            away_rank = LigneRanking.objects.filter(team = match.away, ranking__date__lte = match.date).order_by('-ranking__date').first()
            
            # home_stats = match.get_home_before_stats()
            # away_stats = match.get_away_before_stats()
            
            # if home_stats is None or away_stats is None:
            #     continue
            
            # min_points = min(home_stats.points, away_stats.points)
            

            ############################################################################################################################
            # HOME NE PERD LE MATCH
            ############################################################################################################################
           



            ############################################################################################################################
            # AWAY NE PERD LE MATCH
            ############################################################################################################################
            # if pts_h * 2  <= pts_a and away_stats.points > home_stats.points * 2.5:
            #     PredictionTest.objects.create(
            #         mode = ModePrediction.get("M0"),
            #         type = TypePrediction.get("X2"),
            #         match = match,
            #         pct = 85
            #     )
            
            

            p = footstats.plus_but(home_last_matchs, 2.5) + footstats.plus_but(away_last_matchs, 2.5)
            m = footstats.moins_but(home_last_matchs, 2.5) + footstats.moins_but(away_last_matchs, 2.5)
            if p + m  < 15 :
                continue
            ############################################################################################################################
            # PLUS DE 1.5 BUTS DANS LE MATCH
            ############################################################################################################################
            if (p > m+1) and (home_rank.avg_gs + away_rank.avg_gs) >= 2.8 :
                PredictionTest.objects.create(
                    mode = ModePrediction.get("M0"),
                    type = TypePrediction.get("p1_5"),
                    match = match,
                    pct = round((p / 20 ), 2) * 100
                )
            
            

            ############################################################################################################################
            # MOINS DE 3.5 BUTS DANS LE MATCH
            ############################################################################################################################
            if (m > p+1) and (home_rank.avg_ga + away_rank.avg_ga) <= 2  and (home_rank.avg_gs + away_rank.avg_gs) < 3:
                PredictionTest.objects.create(
                    mode = ModePrediction.get("M0"),
                    type = TypePrediction.get("m3_5"),
                    match = match,
                    pct = round((p / 20 ), 2) * 100
                )
            
            
            

            # ############################################################################################################################
            # # HOME VA MARQUER AU MOINS UN BUT
            # ############################################################################################################################
            # if avg_goals_scored_h >= 1.5 and avg_goals_conceded_a >= 1.2 :
            #     # fact = home_facts.filter(type = TypeFact.objects.get(name = "GS")).first()
            #     # if fact is not None and fact.pct >= 75 :
            #     PredictionTest.objects.create(
            #         mode = ModePrediction.get("M0"),
            #         type = TypePrediction.get("HG"),
            #         match = match,
            #         pct = 85
            #     )
            
            
            

            # ############################################################################################################################
            # # AWAY VA MARQUER AU MOINS UN BUT
            # ############################################################################################################################
            # if avg_goals_scored_a >= 1.5 and avg_goals_conceded_h >= 1.5 :
            #     fact_h = away_facts.filter(type = TypeFact.objects.get(name = "GC")).first()
            #     fact_a = away_facts.filter(type = TypeFact.objects.get(name = "GS")).first()
            #     facctt = away_facts.filter(type = TypeFact.objects.get(name = "TGS")).first()
            #     if (fact_h is not None and fact_h.pct >= 80) and (fact_a is not None and fact_a.pct >= 80) and facctt is not None and facctt.pct >= 100 :
            #         PredictionTest.objects.create(
            #             mode = ModePrediction.get("M0"),
            #             type = TypePrediction.get("AG"),
            #             match = match,
            #             pct = 85
            #         )
            
            
            

            # ############################################################################################################################
            # # MOINS DE 1.5 BUTS A LA MI-TEMPS
            # ############################################################################################################################
            # # if pts_h * 2 <= pts_a :
            # #     PredictionTest.objects.create(
            # #         mode = ModePrediction.get("M0"),
            # #         type = TypePrediction.get("m1_5_MT"),
            # #         match = match,
            # #         pct = 85
            # #     )
            
            
            
            
            

#             if not(home_stats.avg_corners_for == 0 and away_stats.avg_corners_against == 0):
            
#                 total_home = home_stats.avg_corners_for + home_stats.avg_corners_against
#                 avg_home = total_home / 2
#                 total_away = away_stats.avg_corners_for + away_stats.avg_corners_against
#                 avg_away = total_away / 2
#                 # pre = ((home_stats.avg_corners_for or 0) + (home_stats.avg_corners_against or 0) + (away_stats.avg_corners_for or 0) + (away_stats.avg_corners_against or 0)) / 2
#                 # competitionstats = match.edition.edition_stats.filter(ranking__date__lte = match.date).order_by('-created_at').first()

#                 ############################################################################################################################
#                 # MOINS DE 12.5 CORNERS DANS LE MATCH
#                 ############################################################################################################################
#                 if avg_home + avg_away < 9:
#                     PredictionTest.objects.create(
#                         mode = ModePrediction.get("M0"),
#                         type = TypePrediction.get("corner_m12_5"),
#                         match = match,
#                         pct = 85
#                     )

                    
#                 ############################################################################################################################
#                 # PLUS DE 7.5 CORNERS DANS LE MATCH
#                 ############################################################################################################################                   
#                 if  avg_home + avg_away > 12 and total_home >= 11 and total_away >= 11:
#                     PredictionTest.objects.create(
#                         mode = ModePrediction.get("M0"),
#                         type = TypePrediction.get("corner_p6_5"),
#                         match = match,
#                         pct = 85
#                     )
                   
            
                    
#                 ############################################################################################################################
#                 # HOME CORNERS NE PERD PAS LE MATCH
#                 ############################################################################################################################                   
#                 if home_stats.points > away_stats.points * 3.5:
#                     PredictionTest.objects.create(
#                         mode = ModePrediction.get("M0"),
#                         type = TypePrediction.get("1C"),
#                         match = match,
#                         pct = 85
#                     )
                   
            
                    
#                 ############################################################################################################################
#                 # AWAY CORNERS NE PERD PAS LE MATCH
#                 ############################################################################################################################                   
#                 if home_stats.points < away_stats.points * 3.5:
#                     PredictionTest.objects.create(
#                         mode = ModePrediction.get("M0"),
#                         type = TypePrediction.get("2C"),
#                         match = match,
#                         pct = 85
#                     )
                   
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
#             # m3_5 = p1_5 = moy = 0
#             # matchs_betting = match.similaires_betting(10)
#             # if len(matchs_betting) > 0:
#             #     for x in matchs_betting:
#             #         result = x.get_result()
#             #     moy += (result.home_score + result.away_score) / len(matchs_betting)
#             #     p1_5 = fish_law_plus(moy, 1.5)
#             #     m3_5 = fish_law_moins(moy, 3.5)
            
  
            
#             # pts, ppg_h, scored, avg_goals_scored_h, conceded, avg_goals_conceded_h = match.home.last_stats(match, edition = True, number = 10)
#             # pts, ppg_a, scored, avg_goals_scored_a, conceded, avg_goals_conceded_a = match.away.last_stats(match, edition = True, number = 10)
            
#             # X_test = [[avg_goals_scored_h, avg_goals_scored_a, avg_goals_conceded_h, avg_goals_conceded_a, ppg_h, ppg_a]]
#             # predictions = model_charge.predict(X_test)[0]
#             # total = predictions[0]
#             # sh = predictions[1]
#             # sa = predictions[2]
            
            
#             # home_stats = match.get_home_before_stats()
#             # away_stats = match.get_away_before_stats()
#             # min_points = min(home_stats.points, away_stats.points)
            
#             # avg1 = moyenne_but(avg_goals_scored_h, avg_goals_conceded_a)            
#             # avg2 = moyenne_but(avg_goals_scored_a, avg_goals_conceded_h )
            
#             # datas1 = {}
#             # for x in [0, 1, 2, 3, 4, 5]:
#             #     datas1[x] = bimodal_poisson(avg_goals_scored_h, avg_goals_conceded_a, calcul_p(home_stats.points, away_stats.points), x)
            
#             # datas2 = {}
#             # for x in [0, 1, 2, 3, 4, 5]:
#             #     datas2[x] = bimodal_poisson(avg_goals_scored_a, avg_goals_conceded_h, calcul_p(away_stats.points, home_stats.points), x)
            
#             # datas = {}
#             # for x in datas1:
#             #     for y in datas2:                         
#             #         taux = (datas1[x] * datas2[y] * 100)
#             #         if taux >= 10:
#             #             datas[(x, y)] = round(taux, 2)
#             # datas = sorted(datas.items(), key = lambda x:-x[1])
        
#             # ho = aw = 0
#             # for i, x in enumerate(datas):
#             #     if x[1] > 10 :
#             #         ho += x[0][0]
#             #         aw += x[0][1] 
            

            
            
            
            
#             # ############################################################################################################################
#             # # VOICTOIRE OU NUL DE L4EQUIPE A DOMICILE
#             # ############################################################################################################################
#             # if (sh - sa >= 1) or (sh >= 1.1 and sa <= 0.95):
#             #     PredictionTest.objects.create(
#             #         mode = ModePrediction.get("M0"),
#             #         type = TypePrediction.get("1X"),
#             #         match = match,
#             #         pct = 85
#             #     )
#             # if len(datas) > 2 and ho > aw and home_stats.points-10 > away_stats.points*1.5:
#             #         PredictionTest.objects.create(
#             #             mode = ModePrediction.get("M0"),
#             #             type = TypePrediction.get("1X"),
#             #             match = match,
#             #             pct = 85
#             #         )
#             # if len(datas) == 2 and ho - aw >= 2:
#             #     PredictionTest.objects.create(
#             #         mode = ModePrediction.get("M0"),
#             #         type = TypePrediction.get("1X"),
#             #         match = match,
#             #         pct = 85
#             #     )
            
            
            
            
            
            
            
#             # ############################################################################################################################
#             # # PLUS DE 1,5 BUTS DANS LE MATCH
#             # ############################################################################################################################
#             # if sh + sa >=2.2 and p1_5 >= 85:
#             #     PredictionTest.objects.create(
#             #         mode = ModePrediction.get("M0"),
#             #         type = TypePrediction.get("p1_5"),
#             #         match = match,
#             #         pct = 85
#             #     )
                
            
            
#             # ############################################################################################################################
#             # # MOINS DE 3,5 BUTS DANS LE MATCH
#             # ############################################################################################################################
#             # if abs(sh-sa) < 0.5 and m3_5 >= 87:
#             #     PredictionTest.objects.create(
#             #         mode = ModePrediction.get("M0"),
#             #         type = TypePrediction.get("m3_5"),
#             #         match = match,
#             #         pct = 85
#             #     )
#             # t = 0
#             # for i, x in enumerate(datas):
#             #     if (x[0][0] in [0, 1] and x[0][1] in [0, 1]) and not (x[0][0] == x[0][1] == 1) and i < 4:
#             #         t += x[1]   
#             # if t > 75 and abs(home_stats.points - away_stats.points) < min_points and m3_5 >= 87:
#             #     PredictionTest.objects.create(
#             #         mode = ModePrediction.get("M0"),
#             #         type = TypePrediction.get("m3_5"),
#             #         match = match,
#             #         pct = t
#             #     )
                
            
            
            
            
            
            
            
            
            

                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
# #             if sh >= 1.7:
# #                 PredictionTest.objects.create(
# #                     mode = ModePrediction.get("M0"),
# #                     type = TypePrediction.get("HG"),
# #                     match = match,
# #                     pct = 85
# #                 )
# #             elif sh < 0.8:
# #                 PredictionTest.objects.create(
# #                     mode = ModePrediction.get("M0"),
# #                     type = TypePrediction.get("HG|2"),
# #                     match = match,
# #                     pct = 85
# #                 )
                
                
# #             if sa >= 1.75:
# #                 PredictionTest.objects.create(
# #                     mode = ModePrediction.get("M0"),
# #                     type = TypePrediction.get("AG"),
# #                     match = match,
# #                     pct = 85
# #                 )
# #             elif sa < 0.8:
# #                 PredictionTest.objects.create(
# #                     mode = ModePrediction.get("M0"),
# #                     type = TypePrediction.get("AG|2"),
# #                     match = match,
# #                     pct = 85
# #                 )
                
            

                
            

                
# #             if (sa - sh >= 0.7) and (sa >= 1.3 ):
# #                 PredictionTest.objects.create(
# #                     mode = ModePrediction.get("M0"),
# #                     type = TypePrediction.get("X2"),
# #                     match = match,
# #                     pct = 85
# #                 )
                
                
# #             if total < 2.2 and abs(sh-sa) < 0.5:
# #                 PredictionTest.objects.create(
# #                     mode = ModePrediction.get("M0"),
# #                     type = TypePrediction.get("m3_5"),
# #                     match = match,
# #                     pct = 85
# #                 )
                
                

# #             datas1 = {}
# #             for x in [0, 1, 2, 3, 4, 5]:
# #                 datas1[x] = bimodal_poisson(avg_goals_scored_h, avg_goals_conceded_a, calcul_p(home_stats.points, away_stats.points), x)
# #             # print(datas1)
            
# #             datas2 = {}
# #             for x in [0, 1, 2, 3, 4, 5]:
# #                 datas2[x] = bimodal_poisson(avg_goals_scored_a, avg_goals_conceded_h, calcul_p(away_stats.points, home_stats.points), x)
# #             # print(datas2)
            
            
            
# #             # Calculer la probabilité d'avoir un écart de buts donné
# #             # skellam_proba = {}
# #             # for x in np.arange(-5, 6):
# #             #     skellam_proba[x] = round(skellam.pmf(x, avg_goals_scored_h, avg_goals_conceded_a) * 100, 2)
# #             # print(skellam_proba)
            
            
# #             # skellam_proba = {}
# #             # for x in np.arange(-5, 6):
# #             #     skellam_proba[-x] = round(skellam.pmf(-x, avg_goals_scored_a, avg_goals_conceded_h) * 100, 2)
# #             # print(sorted(skellam_proba.items(), key = lambda x:x[0]))
# #             # break
                
# #             # home_win_proba = np.sum(skellam_proba[6:])
# #             # away_win_proba = np.sum(skellam_proba[:5])
# #             # draw_proba = skellam_proba[5]            


# #             datas = {}
# #             for x in datas1:
# #                 for y in datas2:                         
# #                     taux = (datas1[x] * datas2[y] * 100)
# #                     if taux >= 10:
# #                         datas[(x, y)] = round(taux, 2)
# #             datas = sorted(datas.items(), key = lambda x:-x[1])
            
# #             print(datas)
# #             print("-------------------------------------------")

# #             # for i, x in enumerate(datas):
# #             #     PredictionScore.objects.create(
# #             #         home_score = x[0][0],
# #             #         away_score = x[0][1],
# #             #         match = match,
# #             #         pct = x[1]
# #             #     )
                


# #             # if len(datas) == 0:
# #             #     continue


        
# #             ho = aw = 0
# #             for i, x in enumerate(datas):
# #                 if x[1] > 10 :
# #                     ho += x[0][0]
# #                     aw += x[0][1] 
# #             if len(datas) > 2:
# #                 if ho > aw and home_stats.points-10 > away_stats.points*1.5:
# #                     PredictionTest.objects.create(
# #                         mode = ModePrediction.get("M0"),
# #                         type = TypePrediction.get("1X"),
# #                         match = match,
# #                         pct = 85
# #                     )
# #                 elif ho == 0 and  aw >= 2 and home_stats.points*1.5 < away_stats.points :
# #                     PredictionTest.objects.create(
# #                         mode = ModePrediction.get("M0"),
# #                         type = TypePrediction.get("X2"),
# #                         match = match,
# #                         pct = 85
# #                     )
# #                 elif ho > 2 and abs(ho -aw) > 2 and home_stats.points + away_stats.points >= min_points * 3:
# #                     pass
# #                     PredictionTest.objects.create(
# #                         mode = ModePrediction.get("M0"),
# #                         type = TypePrediction.get("p1_5"),
# #                         match = match,
# #                         pct = 85
# #                     )
                        
                        
# #                 if ho >= 3:
# #                     PredictionTest.objects.create(
# #                         mode = ModePrediction.get("M0"),
# #                         type = TypePrediction.get("HG"),
# #                         match = match,
# #                         pct = 85
# #                     )
# #                 elif aw >= 3 and away_stats.points > min_points :
# #                     PredictionTest.objects.create(
# #                         mode = ModePrediction.get("M0"),
# #                         type = TypePrediction.get("AG"),
# #                         match = match,
# #                         pct = 85
# #                     )
                    
# #             else:
# #                 if abs(ho -aw) <= 1 and abs(home_stats.points - away_stats.points) < min_points:
# #                     for i, x in enumerate(datas):
# #                         if x[0][0] == x[0][1] :
# #                             PredictionTest.objects.create(
# #                                 mode = ModePrediction.get("M0"),
# #                                 type = TypePrediction.get("12"),
# #                                 match = match,
# #                                 pct = 85
# #                             )
# #                             break
                        
# #                 if home_stats.points + away_stats.points >= min_points * 3:
# #                     PredictionTest.objects.create(
# #                         mode = ModePrediction.get("M0"),
# #                         type = TypePrediction.get("p1_5"),
# #                         match = match,
# #                         pct = 85
# #                     )
                    
# #                 if len(datas) == 2 and ho - aw >= 2:
# #                     PredictionTest.objects.create(
# #                         mode = ModePrediction.get("M0"),
# #                         type = TypePrediction.get("1X"),
# #                         match = match,
# #                         pct = 85
# #                     )
                    
                
# #             t = 0
# #             for i, x in enumerate(datas):
# #                 if (x[0][0] in [0, 1] and x[0][1] in [0, 1]) and not (x[0][0] == x[0][1] == 1) and i < 4:
# #                     t += x[1]   
# #             if t > 60 and abs(home_stats.points - away_stats.points) <= min_points :
# #                 PredictionTest.objects.create(
# #                     mode = ModePrediction.get("M0"),
# #                     type = TypePrediction.get("m3_5"),
# #                     match = match,
# #                     pct = t
# #                 )
                

            
            
            
# # ###############################################################################################################################################
# # ###############################################################################################################################################
# # ###############################################################################################################################################
# #             if home_stats.avg_corners_for == 0 and away_stats.avg_corners_against == 0:
# #                 continue
                
# #             # print(match, match.date)
# #             avg1 = (home_stats.avg_corners_for + away_stats.avg_corners_against) /2
# #             # datas1 = {}
# #             # for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
# #             #     t = fish_law(avg, x)
# #             #     if t >= 0.15:
# #             #         datas1[x] = round(t / 100, 2)
# #             # print(datas1)
            
            
# #             avg2 = (away_stats.avg_corners_for + home_stats.avg_corners_against ) / 2
# #             # datas2 = {}
# #             # for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
# #             #     t = fish_law(avg2, x)
# #             #     if t >= 0.15:
# #             #         datas2[x] = round(t / 100, 2)
# #             # print(datas2)
            
# #             # print('--------------------', avg1, avg2)
# #             # datas = {}
# #             # for x in datas1:
# #             #     for y in datas2:
# #             #         taux = datas1[x] * datas2[y] * 100
# #             #         if taux >= 10:
# #             #             datas[(x, y)] = round(taux, 2)
# #             # datas = sorted(datas.items(), key = lambda x:-x[1])

            
# #             # for i, x in enumerate(datas):
# #             #     if x[1] > 10 and i < 4:
# #             #         print(x, x[0][0], x[0][1])
# #                     # PredictionScore.objects.create(
# #                     #     home_score = x[0][0],
# #                     #     away_score = x[0][1],
# #                     #     match = match,
# #                     #     pct = x[1]
# #                     # )
                    

# #             if avg1 + avg2 >= 12:
# #                 PredictionTest.objects.create(
# #                     mode = ModePrediction.get("M0"),
# #                     type = TypePrediction.get("corner_p6_5"),
# #                     match = match,
# #                     pct = 85
# #                 )
                
                
     
     
                    
# #             #         print(x[0] , "******", x[1])
# #             # break
# #             # print("-------------------------------------------------------------------")
# #             # extra = match.get_extra_info_match()
            
# #             competitionstats = match.edition.edition_stats.filter(ranking__date__lte = match.date).order_by('-created_at').first()
# #             home_stats = match.get_home_before_stats()
# #             away_stats = match.get_away_before_stats()
            
# #             if home_stats is not None and away_stats is not None: 
# #                 pre = ((home_stats.avg_corners_for or 0) + (home_stats.avg_corners_against or 0) + (away_stats.avg_corners_for or 0) + (away_stats.avg_corners_against or 0)) / 2
# #                 # out = (extra.home_corners or 0 )+ (extra.away_corners or 0)
# #                 # if not out == 0:
                    
# #                 if 0 < pre >= 14:
# #                     if home_stats.avg_corners_for + away_stats.avg_corners_against >= competitionstats.avg_corners and  home_stats.avg_corners_against + away_stats.avg_corners_for >= competitionstats.avg_corners:
# #                         PredictionTest.objects.create(
# #                             mode = ModePrediction.get("M0"),
# #                             type = TypePrediction.get("corner_p6_5"),
# #                             match = match,
# #                             pct = 85
# #                         )
     