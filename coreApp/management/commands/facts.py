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
            
            while True:
                for match in Match.objects.filter(is_compared = True).exclude(is_facted = True).order_by('date')[:5000]:
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
                        
                    match.is_facted = True
                    match.save()
                    print(match)
                        
                while threading.active_count() > 1:
                    print("en attente ---------------: ", threading.active_count())
                    time.sleep(25)
                self.stdout.write(self.style.SUCCESS('List des matchs facted avec succes !'))    
                    
        except Exception as e:
            print(e)
            