from django.core.management.base import BaseCommand, CommandError
from fixtureApp.models import *
import threading
import os, time, json


def function(instance):
    edition = instance.edition
    matchs = edition.edition_du_match.filter(deleted = False).order_by("date").exclude(date = None)
    if  matchs.first() is not None and matchs.last() is not None:
        edition.start_date =   matchs.first().date  
        edition.finish_date =   matchs.last().date  
        edition.save()
        
        
    for team in [instance.home, instance.away]:
        pts, ppg, scored, avg_goals_scored, conceded, avg_goals_conceded = team.last_stats(instance, edition = True)
        datas = team.extra_info_stats(instance, edition = True)      
        
        BeforeMatchStat.objects.create(
            match                       = instance,
            team                        = instance.home if (instance.home == team) else instance.away,
            ppg                         = ppg,
            goals_scored                = scored,
            avg_goals_scored            = avg_goals_scored,
            goals_conceded              = conceded,
            avg_goals_conceded          = avg_goals_conceded,
            avg_fouls_for               = datas.get("avg_fouls_for", 0),
            avg_fouls_against           = datas.get("avg_fouls_against", 0),
            avg_corners_for             = datas.get("avg_corners_for", 0),
            avg_corners_against         = datas.get("avg_corners_against", 0),
            avg_shots_for               = datas.get("avg_shots_for", 0),
            avg_shots_against           = datas.get("avg_shots_against", 0),
            avg_shots_target_for        = datas.get("avg_shots_target_for", 0),
            avg_shots_target_against    = datas.get("avg_shots_target_against", 0),
            avg_offside_for             = datas.get("avg_offside_for", 0),
            avg_offside_against         = datas.get("avg_offside_against", 0),
            avg_cards_for               = datas.get("avg_cards_for", 0),
            avg_cards_against           = datas.get("avg_cards_against", 0),
        )
    
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:            
            
            while True:
                print("START: Current active thread count ---------------: ", threading.active_count())
                for match in Match.objects.exclude(is_stated = True).order_by('date')[:1000]:
                    while threading.active_count() > 1002:
                        time.sleep(10)
                    
                    p = threading.Thread(target=function, args=(match,))
                    p.setDaemon(True)
                    p.start()
                    time.sleep(0.1)
                    match.is_stated = True
                    match.save()
                    
                print("total compared ---------------: ", Match.objects.filter(is_stated = True).count())
                while threading.active_count() > 1:
                    print("en attente ---------------: ", threading.active_count())
                    time.sleep(25)
                self.stdout.write(self.style.SUCCESS('List des matchs facted avec succes !'))    
                    
        except Exception as e:
            print(e)
            