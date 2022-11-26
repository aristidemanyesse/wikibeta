from django.core.management.base import BaseCommand, CommandError
import csv, os, re
from betting.models import *
from features.models import *
from dateparser import parse


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        
        # for path, dirs, files in os.walk("datas/lot1/england/"):
        #     for dir in dirs:
        #         os.rename("datas/lot1/england/{}/Premier.csv".format(dir), "datas/lot1/england/{}/{}".format(dir, "Premier League.csv"))
        #         print(dir)
        #     break
        
        
        year = 2013
        files = [x for x in os.listdir("datas/lot1/england") if not os.path.isdir("datas/lot1/england/{}".format(x))]
        for file in files:
            nb = re.findall('\d+', file)
            if nb[0] == "1":
                if len(nb) == 1:
                    edition = "{}-{}".format(year, year+1)
                else:
                    edition = "{}-{}".format(year-int(nb[-1]), year-int(nb[-1])+1)
                path = "datas/lot1/england/{}".format(edition)
                os.makedirs(path, exist_ok=True)
                os.rename("datas/lot1/england/{}".format(file), "datas/lot1/england/{}/{}".format(edition, "england SuperLigue.csv"))
                print(edition)


        self.stdout.write(self.style.SUCCESS('Structuration  success ! !'))