from django.core.management.base import BaseCommand, CommandError
import os, time
from .predictions import *
from competitionApp.models import *
import threading
    
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:            
            
            for edit in EditionCompetition.objects.filter():
                if threading.active_count() > 145:
                    time.sleep(360)
                print("START: Current active thread count ---------------: ", threading.active_count())
                
                # p = threading.Thread(target=p1, args=(edit,))
                # p.setDaemon(True)
                # p.start()
                # time.sleep(1)
                
                # p = threading.Thread(target=p2, args=(edit,))
                # p.setDaemon(True)
                # p.start()
                # time.sleep(1)

                # p = threading.Thread(target=p4, args=(edit,))
                # p.setDaemon(True)
                # p.start()
                # time.sleep(1)
                    
            self.stdout.write(self.style.SUCCESS('Base de données initialisée avec succes !'))
            
        except Exception as e:
            print(e)
