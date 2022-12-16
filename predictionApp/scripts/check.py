from django.core.management.base import BaseCommand, CommandError
from predictionApp.models import *
from fixtureApp.models import *


def function(self, *args, **options):
    datas = Prediction.objects.filter(is_checked = None)
    for predict in datas:
        predict.validity()
        print(predict.is_checked)