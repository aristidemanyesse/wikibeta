from django.core.management.base import BaseCommand, CommandError
import csv, os, re
from bettingApp.models import *
from fixtureApp.models import *
from dateparser import parse


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):    
        #restructuration
        dir = "/home/aristide/Téléchargements/wikibet-data"  
        year = 1993
        dirs = [x for x in os.listdir(dir) if os.path.isdir(f"{dir}/{x}")]
        for directory in dirs:
            nb = re.findall('\d+', directory)
            if len(nb) == 0:
                edition = "{}-{}".format(year, year+1)
            else:
                edition = "{}-{}".format(year+int(nb[-1]), year+int(nb[-1])+1)
            path = f"{dir}/{edition}"
            os.rename(f"{dir}/{directory}", f"{dir}/{edition}")
            print(edition, directory)

        self.stdout.write(self.style.SUCCESS('Structuration  success ! !'))