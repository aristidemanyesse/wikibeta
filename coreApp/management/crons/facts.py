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
    


def handle():
    try:      
        for match in Match.objects.filter(is_compared = True).exclude(is_facted = True).order_by('date')[:60]:
            print("START: Current active thread count ---------------: ", threading.active_count())
            while threading.active_count() > 501:
                time.sleep(10)
            
            p1 = threading.Thread(target=get_home_facts.function, args=(match,))
            p1.setDaemon(True)
            p1.start()
            time.sleep(0.01)
            
            p2 = threading.Thread(target=get_away_facts.function, args=(match,))
            p2.setDaemon(True)
            p2.start()
            time.sleep(0.01)
                
            match.is_facted = True
            match.save()
            print(match, match.date)
        
        while threading.active_count() > 1:
            print("en attente ---------------: ", threading.active_count())
            time.sleep(25)  
    except Exception as e:
        print(e)
        