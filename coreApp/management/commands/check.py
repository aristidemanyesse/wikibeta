from django.core.management.base import BaseCommand, CommandError
import os, time
from settings import settings
from .extract_data import save_from_dir, save_from_file
from predictionApp.models import *

import threading
    
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        datas = Prediction.objects.filter(is_checked = None)
        for predict in datas:
            predict.validity()
            print(predict.is_checked)