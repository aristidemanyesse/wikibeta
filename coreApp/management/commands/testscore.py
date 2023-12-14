from django.core.management.base import BaseCommand, CommandError
from coreApp.management.commands.predictionscore import predictscore
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
        PredictionTest.objects.all().delete() 

        matchs = Match.objects.filter(is_finished = True).exclude(is_posted = True).order_by('-date')[:1000]
        
        total = 0
        ok = 0
        tous = 0
        mtotal = 0
        m12 = 0
        for nb, match in enumerate(matchs):
            if len( match.away.get_last_matchs(match, edition = True)) < 4 or len( match.home.get_last_matchs(match, edition = True)) < 4:
                continue
            
            total += 1
            
            result = match.get_result()
            scores = predictscore(match)
            
            home_maitrise = match.home.maitrise(match)
            away_maitrise = match.away.maitrise(match)
            
            tous += len(scores)
            for score in scores:
                if score.home_score == result.home_score and score.away_score == result.away_score:
                    ok += 1
                    break
                
            test = scores[0].total() + scores[1].total()
            if test < 2.5:
                PredictionTest.objects.create(
                    mode = ModePrediction.get("M2"),
                    type = TypePrediction.get("m3_5"),
                    match = match,
                    pct = 85
                )
                
            if test > 4.5:
                PredictionTest.objects.create(
                    mode = ModePrediction.get("M2"),
                    type = TypePrediction.get("p1_5"),
                    match = match,
                    pct = 85
                )
            
            test = [x for x in scores if x.home_score == x.away_score]
            if len(test) ==0:
                PredictionTest.objects.create(
                    mode = ModePrediction.get("M2"),
                    type = TypePrediction.get("12"),
                    match = match,
                    pct = 85
                )
            
            print(result, match.date)
            print("MAI", "\t", home_maitrise , "\t", away_maitrise)
            print(scores)
            print("\n")
        
        print("")
        print(total, tous, ok, mtotal, m12)