from django.core.management.base import BaseCommand, CommandError
import csv, os, re
from betting.models import *
from fixtureApp.models import *
from dateparser import parse



class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        Competition.objects.filter(name = None).delete() 
        Match.objects.filter(away_score = None, home_score = None, result = "").delete() 

  