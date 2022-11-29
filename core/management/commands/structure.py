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
        #         if os.path.exists("datas/lot1/england/{}/Championship.csv".format(dir)) :
        #             os.rename("datas/lot1/england/{}/Championship.csv".format(dir), "datas/lot1/england/{}/{}".format(dir, "England Championship.csv"))
        #             print(dir)
        #     break
        
        
        year = 2023
        files = [x for x in os.listdir("datas/lot1/greece") if not os.path.isdir("datas/lot1/greece/{}".format(x))]
        for file in files:
            nb = re.findall('\d+', file)
            # if len(nb) >= 1 and nb[0] == "1":
            if len(nb) == 0 or nb[0] == 1 or nb[0] == 0:
                edition = "{}-{}".format(year-1, year)
            else:
                edition = "{}-{}".format(year-int(nb[-1])-1, year-int(nb[-1]))
            path = "datas/lot1/greece/{}".format(edition)
            os.makedirs(path, exist_ok=True)
            os.rename("datas/lot1/greece/{}".format(file), "datas/lot1/greece/{}/{}".format(edition, file))
            # "Premier League.csv"
            print(edition, file)


        self.stdout.write(self.style.SUCCESS('Structuration  success ! !'))