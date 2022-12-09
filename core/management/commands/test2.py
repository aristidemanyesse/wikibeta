from django.core.management.base import BaseCommand, CommandError
import csv, os, re
from betting.models import *
from features.models import *
from dateparser import parse
from django.db.models import Q
from fractions import Fraction

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        # test = Fraction(40, 145)
        # print(test, type(test))
        for match in Match.objects.all():
            match.is_finished = True
        #     match.home_half_score = 0
        #     match.away_half_score = 0
        #     match.result_half = "D"
            match.save()