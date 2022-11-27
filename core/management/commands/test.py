from django.core.management.base import BaseCommand, CommandError
import csv, os, re
from betting.models import *
from features.models import *
from dateparser import parse



class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        print(str(None))
        print("" or 12)