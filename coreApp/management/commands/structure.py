from django.core.management.base import BaseCommand, CommandError
import csv, os, re
from betting.models import *
from fixtureApp.models import *
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
        
        
        # for path, dirs, files in os.walk("datas/lot1/scotland/"):
        #     for dir in dirs:
        #         for file in os.listdir("datas/lot1/scotland/{}/".format(dir)):
        #             if file.startswith("SC3"):
        #                 os.rename("datas/lot1/scotland/{}/{}".format(dir, file), "datas/lot1/scotland/{}/{}".format(dir, "Scotland League 2.csv"))
        #             print(dir)
        
        year = 1993
        dirs = [x for x in os.listdir("datas/lot") if os.path.isdir("datas/lot/{}".format(x))]
        for dir in dirs:
            nb = re.findall('\d+', dir)
            # if len(nb) >= 1 and nb[0] == "1":
            if len(nb) == 0:
                edition = "{}-{}".format(year, year+1)
            else:
                edition = "{}-{}".format(year+int(nb[-1]), year+int(nb[-1])+1)
            path = "datas/lot/{}".format(edition)
            # os.makedirs(path, exist_ok=True)
            os.rename("datas/lot/{}".format(dir), "datas/lot/{}".format(edition))
            # "Premier League.csv"
            print(edition, dir)


        self.stdout.write(self.style.SUCCESS('Structuration  success ! !'))