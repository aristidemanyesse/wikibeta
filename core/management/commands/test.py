from django.core.management.base import BaseCommand, CommandError
import csv, os, re
from betting.models import *
from features.models import *
from dateparser import parse



class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        # datas = EditionCompetition.objects.filter()
        # for edit in datas:
        #     matchs = edit.edition_du_match.filter(deleted = False)
        #     for match in matchs:
        #         lot = Match.objects.filter(home = match.home, away = match.away, edition = edit) 
        #         if len(lot) > 1:  
        #             dele = lot[0].delete() 
        #             print(dele)    
        
           
        datas = Match.objects.filter(away_score = None, home_score = None, result = "")
        for edit in datas:
            dele = edit.delete() 
            print(dele)       

            # break