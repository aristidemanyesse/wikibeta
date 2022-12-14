from django.core.management.base import BaseCommand, CommandError
import os, time
import predictionApp.functions.p0 as p0
import predictionApp.functions.p1 as p1
import predictionApp.functions.p2 as p2
import predictionApp.functions.p3 as p3
import predictionApp.functions.p4 as p4
from competitionApp.models import *

import statsApp.get_home_facts as get_home_facts
import statsApp.get_away_facts as get_away_facts

import threading
    
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:            
            
            for edit in EditionCompetition.objects.filter().order_by("-edition__name"):
                print("START: Current active thread count ---------------: ", threading.active_count())
                while threading.active_count() > 120:
                    time.sleep(300)
                
                print(edit)
                p = threading.Thread(target=p0.function, args=(edit,))
                p.setDaemon(True)
                p.start()
                time.sleep(1)
                
                p = threading.Thread(target=p1.function, args=(edit,))
                p.setDaemon(True)
                p.start()
                time.sleep(1)
                
                p = threading.Thread(target=p2.function, args=(edit,))
                p.setDaemon(True)
                p.start()
                time.sleep(1)
                
                p = threading.Thread(target=p3.function, args=(edit,))
                p.setDaemon(True)
                p.start()
                time.sleep(1)

                p = threading.Thread(target=p4.function, args=(edit,))
                p.setDaemon(True)
                p.start()
                time.sleep(1)
                
                
                # for match in edit.edition_du_match.all():
                #     p = threading.Thread(target=get_home_facts.function, args=(match,))
                #     p.setDaemon(True)
                #     p.start()
                #     time.sleep(1)
                    
                #     p = threading.Thread(target=get_away_facts.function, args=(match,))
                #     p.setDaemon(True)
                #     p.start()
                #     time.sleep(1)
                    
                    
            while threading.active_count() > 0:
                print("en attente ---------------: ", threading.active_count())
                time.sleep(30)
            self.stdout.write(self.style.SUCCESS('List des matchs initialis??e avec succes !'))    
                    
        except Exception as e:
            print(e)