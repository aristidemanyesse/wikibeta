from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from competitionApp.models import *
from django.db.models import Avg, Sum, Count
import pytz, threading, time

from extra.ranking import function2

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        
        # for ranking in Ranking.objects.all().order_by('edition'):
        #     if ranking.edition.edition_team.all().count() != ranking.ranking_lignes.all().count():
        #         print(ranking)
        #         ranking.delete()
        
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
        #         edit.start_date =   matchs.first().date  
        #         edit.finish_date =   matchs.last().date  
        #         edit.save()
                
        
        # utc=pytz.UTC
        # date = datetime.now().replace(tzinfo=utc) - timedelta(weeks = 52 * 0)
        # while datetime.now().replace(tzinfo=utc) - timedelta(weeks = 52 * 30) <= date <= datetime.now().replace(tzinfo=utc) - timedelta(weeks = 52 * 0): #ca s'arrete en fevrier 2019, 52 * 4
            
        #     print("START: Current process ---------------: ", threading.active_count())
        #     while threading.active_count() > 500:
        #         time.sleep(200)

        #     print("----------------", date)
        #     p = threading.Thread(target=function2, args=(date,))
        #     p.setDaemon(True)
        #     p.start()
        #     time.sleep(0.5)
            
        #     date = date - timedelta(days = 7)
            
            
        # while threading.active_count() > 1:
        #     print("en attente ---------------: ", threading.active_count())
        #     time.sleep(30)
        # self.stdout.write(self.style.SUCCESS('List des matchs initialisée avec succes !'))  
                
        
        for edi in EditionCompetition.objects.all():
            print("rrrrrrrrrrr", edi)
            ranking = Ranking.objects.create(
                date = edi.start_date,
                edition = edi,
            )
            
            for team in edi.edition_team.all():
                LigneRanking.objects.create(
                    team = team,
                    ranking = ranking,
                    level = 1
                )