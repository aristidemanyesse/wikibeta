from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from competitionApp.models import *
from django.db.models import Avg, Sum, Count
import pytz, threading, time

from extra.ranking import function

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        
        utc=pytz.UTC
        date = datetime(1993, 1, 1).replace(tzinfo=utc)
        while date <= datetime.now().replace(tzinfo=utc):
            
            print("START: Current active thread count ---------------: ", threading.active_count())
            while threading.active_count() > 1200:
                time.sleep(200)

            print("----------------", date)
            p = threading.Thread(target=function, args=(date,))
            p.setDaemon(True)
            p.start()
            time.sleep(0.5)
            
            date = date + timedelta(days = 7)
            
            
        while threading.active_count() > 0:
            print("en attente ---------------: ", threading.active_count())
            time.sleep(30)
        self.stdout.write(self.style.SUCCESS('List des matchs initialisée avec succes !'))  
