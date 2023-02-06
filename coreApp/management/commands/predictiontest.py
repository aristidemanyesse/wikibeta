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

import threading
import os, time
    
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for match in Match.objects.filter(is_finished = True).order_by('-date')[:5000]:
            
            home_stats = match.get_home_before_stats()
            away_stats = match.get_away_before_stats()
            extra = match.get_extra_info_match()
            
            competitionstats = match.edition.edition_stats.filter(ranking__date__lte = match.date).order_by('-created_at').first()

            
            if home_stats is not None and away_stats is not None: 
                pre = ((home_stats.avg_corners_for or 0) + (home_stats.avg_corners_against or 0) + (away_stats.avg_corners_for or 0) + (away_stats.avg_corners_against or 0)) / 2
                # out = (extra.home_corners or 0 )+ (extra.away_corners or 0)
                # if not out == 0:
                    
                if 0 < pre >= 14:
                    if home_stats.avg_corners_for + away_stats.avg_corners_against >= competitionstats.avg_corners and  home_stats.avg_corners_against + away_stats.avg_corners_for >= competitionstats.avg_corners:
                        PredictionTest.objects.create(
                            mode = ModePrediction.get("M0"),
                            type = TypePrediction.get("corner_p8_5"),
                            match = match,
                            pct = 95
                        )
                    
                    print("--------------------------", match, pre)
                    # if 0 < pre < 9:
                    #     if home_stats.avg_corners_for < 10 and home_stats.avg_corners_against < 10 and  away_stats.avg_corners_for < 10 and away_stats.avg_corners_against < 10 :
                    #         Prediction.objects.create(
                    #             mode = ModePrediction.get("M0"),
                    #             type = TypePrediction.get("corner_m12_5"),
                    #             match = match,
                    #             pct = 95
                    #         )
                            
                    