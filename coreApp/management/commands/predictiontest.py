from django.core.management.base import BaseCommand, CommandError
from competitionApp.models import *
from coreApp.management.commands.predictionscore import predictscore
from predictionApp.models import *
from coreApp.templatetags import footstats
from predictionApp.functions import p1, p0, p3, p4

import threading, time



def predict(match):
    
    try:
        if len( match.away.get_last_matchs(match, edition = True)) < 4 or len( match.home.get_last_matchs(match, edition = True)) < 4:
            return
        
        print( match, match.date)
        

        
    except Exception as e:
        print(e)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            PredictionTest.objects.all().delete()            
            PredictionScore.objects.all().delete()            
            for match in Match.objects.filter(is_finished = False).order_by('-date')[:1000]:
                print("START: Current active thread count ---------------: ", threading.active_count())
                while threading.active_count() > 250:
                    time.sleep(10)
                    
                pv = threading.Thread(target=p0.prediction, args=(match,))
                pv.setDaemon(True)
                pv.start()
                time.sleep(0.1)
                
                p = threading.Thread(target=p1.prediction, args=(match,))
                p.setDaemon(True)
                p.start()
                time.sleep(0.1)
                
                
                pv = threading.Thread(target=p3.prediction, args=(match,))
                pv.setDaemon(True)
                pv.start()
                time.sleep(0.1)
                
                pv = threading.Thread(target=p4.prediction, args=(match,))
                pv.setDaemon(True)
                pv.start()
                time.sleep(0.1)
                
                # pg = threading.Thread(target=predictscore, args=(match,))
                # pg.setDaemon(True)
                # pg.start()
                # time.sleep(0.1)
                
                
                print(match)
                    
            while threading.active_count() > 1:
                print("en attente ---------------: ", threading.active_count())
                time.sleep(25)
            self.stdout.write(self.style.SUCCESS('List des matchs facted avec succes !'))    
                
        except Exception as e:
            print(e)
            
     

