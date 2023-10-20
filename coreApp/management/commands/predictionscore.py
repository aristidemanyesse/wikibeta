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



def predict(match):
    
    try:
        if len( match.away.get_last_matchs(match, edition = True)) < 4 or len( match.home.get_last_matchs(match, edition = True)) < 4:
            return
        
        print( match, match.date, match.get_result())
        
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
        


        stats_home = match.get_home_before_stats()
        stats_away = match.get_away_before_stats()
        scores_exacts = []
        for home, p in json.loads(stats_home.expected_goals).items():
            for away, j in json.loads(stats_away.expected_goals).items():
                s = PredictionScore(
                    home_score = int(home),
                    away_score = int(away),
                    pct =  round(p*j, 6)
                )
                scores_exacts.append(s)
        scores_exacts = sorted(scores_exacts, key=lambda x: -x.pct)

        ############################################################################################################################
        # HOME NE PERD LE MATCH
        ############################################################################################################################
        if (home_stats.probabilite_elo > 0.6):
            for score in scores_exacts :
                if score.home_score >= score.away_score:
                    score.pct *= 2
                else:
                    score.pct *= (1+home_stats.probabilite_elo)
    



        ############################################################################################################################
        # AWAY NE PERD LE MATCH
        ############################################################################################################################
        if (away_stats.probabilite_elo > 0.6):
            for score in scores_exacts :
                if score.home_score <= score.away_score:
                    score.pct *= 1.8
                else:
                    score.pct *= (1+away_stats.probabilite_elo)
        

        p = footstats.plus_but(home_last_matchs, 2.5) + footstats.plus_but(away_last_matchs, 2.5)
        m = footstats.moins_but(home_last_matchs, 2.5) + footstats.moins_but(away_last_matchs, 2.5)

        ############################################################################################################################
        # PLUS DE 1.5 BUTS DANS LE MATCH
        ############################################################################################################################
        if (p > m+1) and (home_rank.avg_gs + away_rank.avg_gs) >= 2.8 :
            for score in scores_exacts :
                if score.home_score + score.away_score > 2.5:
                    score.pct *= 1.85
                else:
                    score.pct /= 1.5
            
        if  home_stats.ppg >= 2 and away_stats.ppg >= 2 and ((home_rank.avg_ga + away_rank.avg_ga) >= 2.5):
            for score in scores_exacts :
                if score.home_score + score.away_score > 2.5:
                    score.pct *= 1.80
                else:
                    score.pct /= 1.5

        
        
        ############################################################################################################################
        # MOINS DE 3.5 BUTS DANS LE MATCH
        ############################################################################################################################
        if (m > p+1) and (home_rank.avg_ga + away_rank.avg_ga) <= 2  and (home_rank.avg_gs + away_rank.avg_gs) < 3 :
            for score in scores_exacts :
                if score.home_score + score.away_score < 2.5:
                    score.pct *= 1.80
                    
                    
        if  home_stats.ppg >= 2 and away_stats.ppg >= 2 and (0.40 < home_stats.probabilite_elo < 0.6):
            for score in scores_exacts :
                if score.home_score + score.away_score < 2.5:
                    score.pct *= 1.80
                else:
                    score.pct /= 1.5
        
        
        

        # ############################################################################################################################
        # # HOME VA MARQUER AU MOINS UN BUT
        # ############################################################################################################################
        if avg_goals_scored_h >= 1.5 and avg_goals_conceded_a >= 1.2 :
            for score in scores_exacts :
                if score.home_score  > 0:
                    score.pct *= 1.85
                else:
                    score.pct /= 1.5
        



        btts = footstats.btts(home_last_matchs) + footstats.btts(away_last_matchs)
        cs = footstats.cs(home_last_matchs) + footstats.cs(away_last_matchs)
        
        if btts > ((len(home_last_matchs) + len (away_last_matchs)) / 2):
            for score in scores_exacts :
                if score.home_score  > 0 and score.away_score > 0:
                    score.pct *= 1.85
                    
                    
        
        if btts > ((len(home_last_matchs) + len (away_last_matchs)) / 2):
            for score in scores_exacts :
                if score.home_score  != score.away_score:
                    score.pct *= 1.85
            
                    
        
        # if home_stats.ga_expected >= 2:
        #     for score in scores_exacts :
        #         if score.away_score >= 2:
        #             score.pct *= 1.8
        
        # if home_stats.gs_expected <= 0.8:
        #     for score in scores_exacts :
        #         if score.home_score >= 2:
        #             score.pct /= 1.5
                    
                    
        # if away_stats.ga_expected >= 2:
        #     for score in scores_exacts :
        #         if score.home_score >= 2:
        #             score.pct *= 1.8
                    
        # if away_stats.gs_expected <= 0.8:
        #     for score in scores_exacts :
        #         if score.away_score >= 2:
        #             score.pct /= 1.5
            

        

        
        scores_exacts = sorted(scores_exacts, key=lambda x: -x.pct)
        for score in scores_exacts[:3]:
            print(score)
            score.match = match
            score.save()
 
        
        
    
    except Exception as e:
        print(e)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            PredictionScore.objects.all().delete()            
            # PredictionTest.objects.all().delete()            
            for match in Match.objects.filter().order_by('-date')[:1000]:
                print("START: Current active thread count ---------------: ", threading.active_count())
                while threading.active_count() > 200:
                    time.sleep(30)
                    
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
                    
            while threading.active_count() > 1:
                print("en attente ---------------: ", threading.active_count())
                time.sleep(25)
            self.stdout.write(self.style.SUCCESS('List des matchs facted avec succes !'))    
                
        except Exception as e:
            print(e)
            
     

