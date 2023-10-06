from datetime import datetime
from competitionApp.models import *

import statsApp.get_home_facts as get_home_facts
import statsApp.get_away_facts as get_away_facts

import threading
import os, time
    


def handle():
    try:    
        print("--------------------------------", datetime.now())   
        for match in Match.objects.filter(is_facted = False).order_by('-date')[:20]:
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
            time.sleep(10) 
        print("okkkkkkk") 
            
    except Exception as e:
        match.is_facted = False
        match.save()
        print(e)
        