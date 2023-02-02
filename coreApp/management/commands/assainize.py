from django.core.management.base import BaseCommand, CommandError
from bettingApp.models import *
from fixtureApp.models import *
from statsApp.models import *
from competitionApp.models import *
from dateparser import parse
import threading
import time
from datetime import datetime, timedelta
    

class Command(BaseCommand):


    def handle(self, *args, **options):
        Ranking.objects.all().delete()
        pass
        # Match.objects.filter(created_at__gte = datetime.now() - timedelta(hours= 1)).delete()
        # Competition.objects.filter(created_at__gte = datetime.now() - timedelta(hours= 1)).delete()
        
        # for ligne in LigneRanking.objects.all():
        #     ligne.level += 1
        #     ligne.save() 
        
        # matchs = Match.objects.filter().order_by("-date")[:5000]
        # for match in matchs:
        #     while threading.active_count() >= 35:
        #         time.sleep(30)
        #     print(match, "en attente ---------------: ", threading.active_count())
        #     p = threading.Thread(target=match.save)
        #     p.setDaemon(True)
        #     p.start()
    
        # while threading.active_count() > 0:
        #     print("en attente ---------------: ", threading.active_count())
        #     time.sleep(10)

            
        # datas = Competition.objects.filter()
        # for comp in datas:
        #     comp.logo = "static/images/competitions/default.png"
        #     comp.save()
            
        # datas = Team.objects.filter()
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
                

  