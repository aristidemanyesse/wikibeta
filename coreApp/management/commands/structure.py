from django.core.management.base import BaseCommand, CommandError
import csv, os, re
from bettingApp.models import *
from fixtureApp.models import *
from dateparser import parse


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        year = 1993
        dirs = [x for x in os.listdir("datas/lot") if os.path.isdir("datas/lot/{}".format(x))]
        for dir in dirs:
            nb = re.findall('\d+', dir)
            if len(nb) == 0:
                edition = "{}-{}".format(year, year+1)
            else:
                edition = "{}-{}".format(year+int(nb[-1]), year+int(nb[-1])+1)
            path = "datas/lot/{}".format(edition)
            os.rename("datas/lot/{}".format(dir), "datas/lot/{}".format(edition))
            print(edition, dir)


        self.stdout.write(self.style.SUCCESS('Structuration  success ! !'))