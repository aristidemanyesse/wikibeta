from django.core.management.base import BaseCommand, CommandError
import csv, os, re
from bettingApp.models import *
from fixtureApp.models import *
from statsApp.models import *
from competitionApp.models import *
from dateparser import parse


class Command(BaseCommand):


    def handle(self, *args, **options):
        datas = EditionCompetition.objects.filter()
        for edit in datas:
            matchs = edit.edition_du_match.filter(deleted = False).order_by("date").exclude(date = None)
            if  matchs.first() is not None and matchs.last() is not None:
                print(len(matchs), matchs.first().date, matchs.last().date) 
                edit.start_date =   matchs.first().date  
                edit.finish_date =   matchs.last().date  
                edit.save()
            
        #     # break
        # Competition.objects.filter(name = None).delete() 
        # # ResultMatch.objects.filter(match__away_score = None, match__home_score = None, result = "").delete() 
        # OddsMatch.objects.filter(home = 0).delete() 
        
        
        # for match in Match.objects.all():
        #     result = match.get_result()
        #     if result and result.away_score is None:
        #         match.delete()
                
        #     if result.away_score == result.home_score == 0:
        #         result.home_half_score = 0
        #         result.away_half_score = 0
        #         result.result_half = "D"
        #         result.save()
                
                
        # datas = EditionCompetition.objects.filter()
        # for edit in datas:
        #     matchs = edit.edition_du_match.filter(deleted = False).order_by("date").exclude(date = None)
        #     edit.start_date   = matchs.first().date
        #     edit.finish_date  = matchs.last().date
        #     edit.save()

  