from django.core.management.base import BaseCommand, CommandError
import predictionApp.functions.p0 as p0
import predictionApp.functions.p1 as p1
import predictionApp.functions.p2 as p2
import predictionApp.functions.p3 as p3
import predictionApp.functions.p4 as p4
from competitionApp.models import *

import statsApp.get_home_facts as get_home_facts
import statsApp.get_away_facts as get_away_facts

import threading
import os, time
    
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:            
            
            for match in Match.objects.exclude(is_facted = True, is_predict = True).order_by('date')[:5000]:
                print("START: Current active thread count ---------------: ", threading.active_count())
                while threading.active_count() > 300:
                    time.sleep(10)
                
                if match.match_facts.filter().count() == 0 :
                    p = threading.Thread(target=get_home_facts.function, args=(match,))
                    p.setDaemon(True)
                    p.start()
                    time.sleep(0.01)
                    
                    p = threading.Thread(target=get_away_facts.function, args=(match,))
                    p.setDaemon(True)
                    p.start()
                    time.sleep(0.01)
                    
                
                if match.prediction_match.filter().count() == 0 :
                    p = threading.Thread(target=p0.predict, args=(match,))
                    p.setDaemon(True)
                    p.start()
                    time.sleep(0.01)
                    
                    p = threading.Thread(target=p1.predict, args=(match,))
                    p.setDaemon(True)
                    p.start()
                    time.sleep(0.01)
                    
                    p = threading.Thread(target=p2.predict, args=(match,))
                    p.setDaemon(True)
                    p.start()
                    time.sleep(0.01)
                    
                    p = threading.Thread(target=p3.predict, args=(match,))
                    p.setDaemon(True)
                    p.start()
                    time.sleep(0.01)

                    p = threading.Thread(target=p4.predict, args=(match,))
                    p.setDaemon(True)
                    p.start()
                    time.sleep(0.01)
                
                match.is_facted = True
                match.is_predict = True
                match.save()
                
                print(match)
                    
                
                    
            while threading.active_count() > 0:
                print("en attente ---------------: ", threading.active_count())
                time.sleep(10)
            self.stdout.write(self.style.SUCCESS('List des matchs initialisée avec succes !'))    
                    
        except Exception as e:
            print(e)