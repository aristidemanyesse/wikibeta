import threading, time, json
from datetime import datetime
from statsApp.models import  TeamProfileMatch
from fixtureApp.models import Match

def proifle(instance):
    try:
        for team in [instance.home, instance.away]:
            ranking = team.team_lignes_rankings.filter(deleted = False).order_by("-ranking__date").first()
            TeamProfileMatch.objects.create(
                team        = team,
                match       = instance,
                dynamique   = team.dynamique(instance),
                attack      = team.attaque(instance),
                defense     = team.defense(instance),
                maitrise    = team.maitrise(instance),
                ranking     = (21 - ranking.level) if ranking is not None else 10 
            )
        
        print(instance, instance.date)
    
    except Exception as e:
        print("Erreur: before function", e)  
        
        
        
def handle():
    try:    
        print("--------------------------------", datetime.now()) 
        # TeamProfileMatch.objects.all().delete()
        # Match.objects.filter(is_profiled = True).update(is_profiled = False)
        for match in Match.objects.filter(is_profiled = False).order_by('-date')[:300]:
            # print("START: Current active thread count ---------------: ", threading.active_count())
            while threading.active_count() > 310:
                time.sleep(10)
            
            p1 = threading.Thread(target=proifle, args=(match,))
            p1.setDaemon(True)
            p1.start()
            
            match.is_profiled = True
            match.save()
        
        while threading.active_count() > 1:
            # print("en attente ---------------: ", threading.active_count())
            time.sleep(10)  
        print("okkkkk !!!")
            
    except Exception as e:
        print(e)  
