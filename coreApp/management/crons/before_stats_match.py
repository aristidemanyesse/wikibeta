from django.core.management.base import BaseCommand, CommandError
from fixtureApp.models import *
import threading, math
import os, time, json


def function(instance):
    list_intercepts            = json.dumps([str(x.id) for x in instance.similaires_intercepts(10)])
    list_confrontations        = json.dumps([str(x.id) for x in instance.confrontations_directes(10)])
    list_similaires_ppg        = json.dumps([str(x.id) for x in instance.similaires_ppg(10)])
    list_similaires_ppg2       = json.dumps([str(x.id) for x in instance.similaires_ppg2(10)])
    list_similaires_betting    = json.dumps([str(x.id) for x in instance.similaires_betting(10)])
    home_stats, away_stats = instance.get_home_before_stats(), instance.get_away_before_stats()
    for stats in [home_stats, away_stats]:
        stats.score_elo                                     = stats.team.elo_score(instance)
        stats.total_gs_expected, stats.total_ga_expected,   = stats.team.expected_goals(instance)
        stats.list_intercepts                               = list_intercepts
        stats.list_confrontations                           = list_confrontations
        stats.list_similaires_ppg                           = list_similaires_ppg
        stats.list_similaires_ppg2                          = list_similaires_ppg2
        stats.list_similaires_betting                       = list_similaires_betting
        stats.save()
    
    home_last_matchs = instance.home.get_last_matchs(instance, edition = True)
    away_last_matchs = instance.away.get_last_matchs(instance, edition = True)
        
    home_stats.score_elo += abs(home_stats.score_elo - away_stats.score_elo) * 0.07
    proba = 1 / (1 + 10 ** ((away_stats.score_elo - home_stats.score_elo) / 400))
    
    test = len(home_last_matchs) > 0 and len(away_last_matchs) > 0
    home_stats.probabilite_elo = proba
    home_stats.gs_expected = round(((home_stats.total_gs_expected / len(home_last_matchs)) + (away_stats.total_ga_expected / len(away_last_matchs))) / 2, 3) if test else 1 
    home_stats.ga_expected = round(((home_stats.total_ga_expected / len(home_last_matchs)) + (away_stats.total_gs_expected / len(away_last_matchs))) / 2, 3) if test else 1 
    home_stats.save()
    
    away_stats.probabilite_elo = 1 - proba
    away_stats.gs_expected = round(((away_stats.total_gs_expected / len(away_last_matchs)) + (home_stats.total_ga_expected / len(home_last_matchs))) / 2, 3) if test else 1 
    away_stats.ga_expected = round(((away_stats.total_ga_expected / len(away_last_matchs)) + (home_stats.total_gs_expected / len(home_last_matchs))) / 2, 3) if test else 1 
    away_stats.save()
    
        
    
def handle():
    try:            
        for match in Match.objects.filter(is_compared = False).order_by('-date')[:60]:
            while threading.active_count() > 105:
                time.sleep(10)
            
            p = threading.Thread(target=function, args=(match,))
            p.setDaemon(True)
            p.start()
            time.sleep(0.1)
            match.is_compared = True
            match.save()
            print(match, match.date)
                
        while threading.active_count() > 1:
            print("en attente ---------------: ", threading.active_count())
            time.sleep(25)
    except Exception as e:
        print(e)