from django.core.management.base import BaseCommand, CommandError
from fixtureApp.models import *
import threading
import os, time, json


def function(instance):
    list_intercepts            = json.dumps([str(x.id) for x in instance.similaires_intercepts(10)])
    list_confrontations        = json.dumps([str(x.id) for x in instance.confrontations_directes(10)])
    list_similaires_ppg        = json.dumps([str(x.id) for x in instance.similaires_ppg(10)])
    list_similaires_ppg2       = json.dumps([str(x.id) for x in instance.similaires_ppg2(10)])
    list_similaires_betting    = json.dumps([str(x.id) for x in instance.similaires_betting(10)])
    for stats in [instance.get_home_before_stats(), instance.get_away_before_stats()]:
        stats.points                     = stats.team.fight_points(instance)
        stats.list_intercepts            = list_intercepts
        stats.list_confrontations        = list_confrontations
        stats.list_similaires_ppg        = list_similaires_ppg
        stats.list_similaires_ppg2       = list_similaires_ppg2
        stats.list_similaires_betting    = list_similaires_betting
        stats.save()
        
    
def handle():
    try:            
        
        for match in Match.objects.filter(is_compared = False).order_by('-date')[:20]:
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