import threading, time, json
from datetime import datetime
from coreApp.functions import bimodal_poisson
from statsApp.models import BeforeMatchStat
from fixtureApp.models import Match

def compared(instance):
    try:
        list_intercepts            = json.dumps([str(x.id) for x in instance.similaires_intercepts(10)])
        list_confrontations        = json.dumps([str(x.id) for x in instance.confrontations_directes(10)])
        list_similaires_ppg        = json.dumps([str(x.id) for x in instance.similaires_ppg(10)])
        list_similaires_ppg2       = json.dumps([str(x.id) for x in instance.similaires_ppg2(10)])
        list_similaires_betting    = json.dumps([str(x.id) for x in instance.similaires_betting(10)])
        home_stats, away_stats = instance.get_home_before_stats(), instance.get_away_before_stats()
        for stats in [home_stats, away_stats]:
            stats.list_intercepts                               = list_intercepts
            stats.list_confrontations                           = list_confrontations
            stats.list_similaires_ppg                           = list_similaires_ppg
            stats.list_similaires_ppg2                          = list_similaires_ppg2
            stats.list_similaires_betting                       = list_similaires_betting
            stats.save()
        
        print(instance, instance.date)
    
    except Exception as e:
        print("Erreur: before function", e)  
        
        
        
def handle():
    # Match.objects.filter(is_compared_elo = True).update(is_compared_elo = False)
    # Match.objects.filter(is_compared = True).update(is_compared = False)
    # print("textxet")
    
    # for stat in BeforeMatchStat.objects.filter(score_elo__lte = 1300, match__is_compared = True):
    #     print(stat.match)
    #     stat.match.is_compared = False
    #     stat.match.save()
    try:    
        print("--------------------------------", datetime.now()) 
        for match in Match.objects.filter(is_compared = False).order_by('date')[:20]:
            print("START: Current active thread count ---------------: ", threading.active_count())
            while threading.active_count() > 501:
                time.sleep(10)
            
            p1 = threading.Thread(target=compared, args=(match,))
            p1.setDaemon(True)
            p1.start()
            time.sleep(0.01)
            
            match.is_compared = True
            match.is_stated = True
            match.save()
        
        while threading.active_count() > 1:
            print("en attente ---------------: ", threading.active_count())
            time.sleep(10)  
        print("okkkkk !!!")
            
    except Exception as e:
        print(e)  






def compared_elo(instance):
    
    try:
        home_stats, away_stats = instance.get_home_before_stats(), instance.get_away_before_stats()
        for stats in [home_stats, away_stats]:
            stats.score_elo                         = stats.team.elo_score(instance)
            stats.gs_expected, stats.ga_expected,   = stats.team.calcul_expected_goals(instance)
            stats.save()
            
        home_stats.score_elo += (BeforeMatchStat.SCORE_ELO_FACTOR / 6) # avantage à domicile
        proba = round((1 / (1 + 10 ** ((away_stats.score_elo - home_stats.score_elo) / 400))), 2)
        
        home_stats.probabilite_elo = proba
        home_stats.expected_goals = json.dumps(bimodal_poisson(home_stats.gs_expected, away_stats.ga_expected))  
        home_stats.save()
        
        away_stats.probabilite_elo = 1 - proba
        away_stats.expected_goals = json.dumps(bimodal_poisson(away_stats.gs_expected, home_stats.ga_expected))
        away_stats.save()
        
        
        print(instance, instance.date)
    
    except Exception as e:
        print("Erreur: before function", e) 


def handle2():
    # Match.objects.filter(is_compared_elo = True).update(is_compared_elo = False)
    try:    
        print("--------------------------------", datetime.now()) 
        for match in Match.objects.filter(is_compared_elo = False).order_by('date')[:15]:
            print("START: Current active thread count ---------------: ", threading.active_count())
            while threading.active_count() > 501:
                time.sleep(10)
            
            p1 = threading.Thread(target=compared_elo, args=(match,))
            p1.setDaemon(True)
            p1.start()
            time.sleep(0.01)
            
            match.is_compared_elo = True
            match.save()
        
        while threading.active_count() > 1:
            print("en attente ---------------: ", threading.active_count())
            time.sleep(10)  
        print("okkkkk !!!")
            
    except Exception as e:
        print(e)  




