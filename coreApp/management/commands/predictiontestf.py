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
        

        matchs = Match.objects.filter(is_finished = True).exclude(is_posted = True).order_by("-date")[:15000]
        
        for nb, match in enumerate(matchs):
            try:
                if len( match.away.get_last_matchs(match, edition = True)) < 4 or len( match.home.get_last_matchs(match, edition = True)) < 4:
                    continue
                
                print(nb, match, match.date)
                
                # competitionstats = match.edition.edition_stats.filter(ranking__date__lte = match.date).order_by('-created_at').first()
                home_last_matchs = match.home.get_last_matchs(match, number = 10, edition = True)
                away_last_matchs = match.away.get_last_matchs(match, number = 10, edition = True)
                
                pts_h, ppg, scored, avg_goals_scored_h, conceded, avg_goals_conceded_h = match.home.last_stats(match, edition = True, number = 5)
                pts_a, ppg, scored, avg_goals_scored_a, conceded, avg_goals_conceded_a = match.away.last_stats(match, edition = True, number = 5)
                
                home_facts = match.match_facts.filter(team = match.home)
                away_facts = match.match_facts.filter(team = match.away)
                
                home_rank = LigneRanking.objects.filter(team = match.home, ranking__date__lte = match.date).order_by('-ranking__date').first()
                away_rank = LigneRanking.objects.filter(team = match.away, ranking__date__lte = match.date).order_by('-ranking__date').first()
                
                home_stats = match.get_home_before_stats()
                away_stats = match.get_away_before_stats()
                
                if home_stats is None or away_stats is None:
                    continue
                
                # min_points = min(home_stats.points, away_stats.points)
                

                ############################################################################################################################
                # HOME NE PERD LE MATCH
                ############################################################################################################################
                if (home_stats.probabilite_elo > 0.6):
                    PredictionTest.objects.create(
                        mode = ModePrediction.get("M0"),
                        type = TypePrediction.get("1X"),
                        match = match,
                        pct = 0.85
                    )
            



                ############################################################################################################################
                # AWAY NE PERD LE MATCH
                ############################################################################################################################
                if pts_h * 2  <= pts_a and away_stats.points > home_stats.points * 2.5:
                    PredictionTest.objects.create(
                        mode = ModePrediction.get("M0"),
                        type = TypePrediction.get("X2"),
                        match = match,
                        pct = 85
                    )
                
                

                p = footstats.plus_but(home_last_matchs, 2.5) + footstats.plus_but(away_last_matchs, 2.5)
                m = footstats.moins_but(home_last_matchs, 2.5) + footstats.moins_but(away_last_matchs, 2.5)
                p4 = footstats.plus_but(home_last_matchs, 3.5) + footstats.plus_but(away_last_matchs, 3.5)
                if p + m  < 15 :
                    continue
                ############################################################################################################################
                # PLUS DE 1.5 BUTS DANS LE MATCH
                ############################################################################################################################
                if (p > m+1) and (home_rank.avg_gs + away_rank.avg_gs) >= 2.8  and p4 > 2:
                    PredictionTest.objects.create(
                        mode = ModePrediction.get("M0"),
                        type = TypePrediction.get("p1_5"),
                        match = match,
                        pct = round((p / 20 ), 2) * 100
                    )
                    
                if  home_stats.ppg >= 2 and away_stats.ppg >= 2 and ((home_rank.avg_ga + away_rank.avg_ga) >= 2.5):
                    PredictionTest.objects.create(
                        mode = ModePrediction.get("M0"),
                        type = TypePrediction.get("p1_5"),
                        match = match,
                        pct = 0.80
                    )

                
                

                ############################################################################################################################
                # MOINS DE 3.5 BUTS DANS LE MATCH
                ############################################################################################################################
                if (m > p+1) and (home_rank.avg_ga + away_rank.avg_ga) <= 2  and (home_rank.avg_gs + away_rank.avg_gs) < 3 and p4 < 5:
                    PredictionTest.objects.create(
                        mode = ModePrediction.get("M0"),
                        type = TypePrediction.get("m3_5"),
                        match = match,
                        pct = round((p / 20 ), 2) * 100
                    )
                if  home_stats.ppg >= 2 and away_stats.ppg >= 2 and (0.40 < home_stats.probabilite_elo < 0.6):
                    PredictionTest.objects.create(
                        mode = ModePrediction.get("M0"),
                        type = TypePrediction.get("m3_5"),
                        match = match,
                        pct = 0.73
                    )
                
                
                

                # ############################################################################################################################
                # # HOME VA MARQUER AU MOINS UN BUT
                # ############################################################################################################################
                if avg_goals_scored_h >= 1.5 and avg_goals_conceded_a >= 1.2 :
                    # fact = home_facts.filter(type = TypeFact.objects.get(name = "GS")).first()
                    # if fact is not None and fact.pct >= 75 :
                    PredictionTest.objects.create(
                        mode = ModePrediction.get("M0"),
                        type = TypePrediction.get("HG"),
                        match = match,
                        pct = 85
                    )
                
                
                

                # ############################################################################################################################
                # # AWAY VA MARQUER AU MOINS UN BUT
                # ############################################################################################################################
                if avg_goals_scored_a >= 1.5 and avg_goals_conceded_h >= 1.5 :
                    fact_h = away_facts.filter(type = TypeFact.objects.get(name = "GC")).first()
                    fact_a = away_facts.filter(type = TypeFact.objects.get(name = "GS")).first()
                    facctt = away_facts.filter(type = TypeFact.objects.get(name = "TGS")).first()
                    if (fact_h is not None and fact_h.pct >= 80) and (fact_a is not None and fact_a.pct >= 80) and facctt is not None and facctt.pct >= 100 :
                        PredictionTest.objects.create(
                            mode = ModePrediction.get("M0"),
                            type = TypePrediction.get("AG"),
                            match = match,
                            pct = 85
                        )
                
                
                

                ############################################################################################################################
                # MOINS DE 1.5 BUTS A LA MI-TEMPS
                ############################################################################################################################
                if pts_h * 2 <= pts_a :
                    PredictionTest.objects.create(
                        mode = ModePrediction.get("M0"),
                        type = TypePrediction.get("m1_5_MT"),
                        match = match,
                        pct = 85
                    )
                
                
                
                
                

                if not(home_stats.avg_corners_for == 0 and away_stats.avg_corners_against == 0):
                
                    total_home = home_stats.avg_corners_for + home_stats.avg_corners_against
                    avg_home = total_home / 2
                    total_away = away_stats.avg_corners_for + away_stats.avg_corners_against
                    avg_away = total_away / 2
                    # pre = ((home_stats.avg_corners_for or 0) + (home_stats.avg_corners_against or 0) + (away_stats.avg_corners_for or 0) + (away_stats.avg_corners_against or 0)) / 2
                    # competitionstats = match.edition.edition_stats.filter(ranking__date__lte = match.date).order_by('-created_at').first()

                    ############################################################################################################################
                    # MOINS DE 12.5 CORNERS DANS LE MATCH
                    ############################################################################################################################
                    if avg_home + avg_away < 9:
                        PredictionTest.objects.create(
                            mode = ModePrediction.get("M0"),
                            type = TypePrediction.get("corner_m12_5"),
                            match = match,
                            pct = 85
                        )

                        
                    ############################################################################################################################
                    # PLUS DE 7.5 CORNERS DANS LE MATCH
                    ############################################################################################################################                   
                    if  avg_home + avg_away > 12 and total_home >= 11 and total_away >= 11:
                        PredictionTest.objects.create(
                            mode = ModePrediction.get("M0"),
                            type = TypePrediction.get("corner_p6_5"),
                            match = match,
                            pct = 85
                        )
                    if (p > m+1) and (home_rank.avg_gs + away_rank.avg_gs) >= 2.8  and p4 > 2:
                        PredictionTest.objects.create(
                            mode = ModePrediction.get("M1"),
                            type = TypePrediction.get("corner_p6_5"),
                            match = match,
                            pct = 85
                        )
                    
                
                        
                    ############################################################################################################################
                    # HOME CORNERS NE PERD PAS LE MATCH
                    ############################################################################################################################                   
                    if home_stats.points > away_stats.points * 3.5:
                        PredictionTest.objects.create(
                            mode = ModePrediction.get("M0"),
                            type = TypePrediction.get("1C"),
                            match = match,
                            pct = 85
                        )
                    
                
                        
                    ############################################################################################################################
                    # AWAY CORNERS NE PERD PAS LE MATCH
                    ############################################################################################################################                   
                    if home_stats.points < away_stats.points * 3.5:
                        PredictionTest.objects.create(
                            mode = ModePrediction.get("M0"),
                            type = TypePrediction.get("2C"),
                            match = match,
                            pct = 85
                        )

                
            except Exception as e:
                print(e)