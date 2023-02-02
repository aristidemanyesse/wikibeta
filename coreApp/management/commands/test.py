from django.core.management.base import BaseCommand, CommandError
from bettingApp.models import *
from fixtureApp.models import *
from statsApp.models import *
from competitionApp.models import *
from dateparser import parse
import threading, datetime
import time
    
    
def main(match):
    print("--------------------------------", match, match.edition)
    confrontations        = json.dumps([str(x.id) for x in match.confrontations_directes(10)])
    similaires_ppg        = json.dumps([str(x.id) for x in match.similaires_ppg(10)])
    similaires_ppg2       = json.dumps([str(x.id) for x in match.similaires_ppg2(10)])
    similaires_betting    = json.dumps([str(x.id) for x in match.similaires_betting(10)])
    
    for stats in [match.get_home_before_stats(), match.get_away_before_stats()]:
        stats.list_confrontations         = confrontations
        stats.list_similaires_ppg         = similaires_ppg
        stats.list_similaires_ppg2        = similaires_ppg2
        stats.list_similaires_betting     = similaires_betting
        stats.save()


class Command(BaseCommand):


    def handle(self, *args, **options):
        for match in Match.objects.filter(date__lte = datetime.datetime.now() - datetime.timedelta(days=3)).order_by('-date'):
            while threading.active_count() >= 800:
                print("processus en cours ---------------: ", threading.active_count())
                time.sleep(5)
            p = threading.Thread(target=main , args=(match,))
            p.setDaemon(True)
            p.start()
            time.sleep(1)
            
        while threading.active_count() > 0:
            print("en attente ---------------: ", threading.active_count())
            time.sleep(30)
        self.stdout.write(self.style.SUCCESS('List des matchs initialisée avec succes !'))  
                                
            



