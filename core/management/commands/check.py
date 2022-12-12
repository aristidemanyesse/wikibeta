from django.core.management.base import BaseCommand, CommandError
import csv, os, re
from prediction.models import *
from features.models import *
from dateparser import parse



class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        datas = Prediction.objects.filter(is_checked = None)
        for predict in datas:
            predict.validity()
            print(predict.is_checked)