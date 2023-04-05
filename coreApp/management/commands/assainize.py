from django.core.management.base import BaseCommand, CommandError
from bettingApp.models import *
from fixtureApp.models import *
from statsApp.models import *
from competitionApp.models import *
from predictionApp.models import *
from dateparser import parse
import threading
import time
from datetime import datetime, timedelta
    

class Command(BaseCommand):


    def handle(self, *args, **options):
        # bad = Competition.objects.get(id = "11525ab3-9628-41d8-bb1d-7eaddb336700")
        # bon = Competition.objects.get(id = "56d269ec-e468-4771-a5fd-84cffbde876f")
        
        # for edit in bad.competition_edition.filter():
        #     edit.competition = bon
        #     edit.save()
        
        
        # PredictionTest.objects.all().delete()
        # Prediction.objects.filter(mode = ModePrediction.get("M0"),
        #     type = TypePrediction.get("corner_m12_5")).delete()
        # for match in Match.objects.all():
        #     if match.before_stat_match.filter().count() != 2:
        #         # match.before_stat_match.filter().delete()
        #         # match.prediction_match.filter().delete()
        #         # match.match_facts.filter().delete()
        #         match.delete()
                
                # print((match.get_result()).__dict__)
                
                # print(match.id, match, match.date)
                # match.save()
        
        # Ranking.objects.all().delete()
        # Match.objects.filter(created_at__gte = datetime.now() - timedelta(hours= 5)).delete()
        pass
        # Competition.objects.filter(created_at__gte = datetime.now() - timedelta(hours= 5)).delete()
        
        
        
        # for ligne in LigneRanking.objects.all():
        #     ligne.level += 1
        #     ligne.save() 
        
        # stats = BeforeMatchStat.objects.filter(points = None).order_by("?")[:1000]
        # for stat in stats:
        #     while threading.active_count() >= 250:
        #         time.sleep(30)
            
        #     try:
        #         print(stat, "----------: ", threading.active_count())
        #         p = threading.Thread(target=stat.mise_a_jour)
        #         p.setDaemon(True)
        #         p.start()
        #         time.sleep(0.01)
        #     except Exception as e:
        #         print(e)
    
        # while threading.active_count() > 1:
        #     print("en attente ---------------: ", threading.active_count())
        #     time.sleep(30)

            
        # datas = Competition.objects.filter()
        # for comp in datas:
        #     comp.logo = "static/images/competitions/default.png"
        #     comp.save()
            
        datas = Fact.objects.all()
        for f in datas:
            f.pct *= 100
            f.save()
            
        # datas = Team.objects.filter(logo = "")
        # for comp in datas:
        #     comp.logo = "static/images/teams/default.png"
        #     comp.save()

            
        # datas = EditionCompetition.objects.filter()
        # for edit in datas:
        #     teams = edit.edition_team.filter()
        #     if len(edit.edition_du_match.filter()) == len(teams) * (len(teams)-1) :
        #         edit.is_finished = True
        #         edit.save()
                
        #     if edit.finish_date is not None and edit.finish_date <= (datetime.now() - timedelta(days = 365)).date() :
        #         edit.is_finished = True
        #         edit.save()
        #     matchs = edit.edition_du_match.filter(deleted = False).order_by("date").exclude(date = None)
        #     if  matchs.first() is not None and matchs.last() is not None:
        #         print(len(matchs), matchs.first().date, matchs.last().date) 
        #         edit.start_date =   matchs.first().date  
        #         edit.finish_date =   matchs.last().date  
        #         edit.save()
            
        #     # break
        # Competition.objects.filter(name = None).delete() 
        # # ResultMatch.objects.filter(match__away_score = None, match__home_score = None, result = "").delete() 
        # OddsMatch.objects.filter(home = 0).delete() 
        
        
        # for match in Match.objects.filter(is_finished = True):
        #     result = match.get_result()
            
        #     if result is None or result.home_score is None or result.away_score is None:
        #         match.delete()
        #         continue
            
        #     home_before = match.get_home_before_stats()
        #     away_before = match.get_away_before_stats()
        #     if home_before is None or away_before is None:
        #         match.delete()
        #         continue
                
        #     elif result.away_score == result.home_score == 0:
        #         result.home_half_score = 0
        #         result.away_half_score = 0
        #         result.result_half = "D"
        #         result.save()
                

  