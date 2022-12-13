import requests
from django.core.management.base import BaseCommand, CommandError
from prediction.models import *
from fixtureApp.models import *
from dateparser import parse

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        url = ['https://www.football-data.co.uk/mmz4281/2223/Latest_Results.csv', "https://www.football-data.co.uk/new/Latest_Results.csv"]
        for i, u in enumerate(url):
            response = requests.get(u)
            with open('datas/results/data_{}.csv'.format(i), 'wb') as file:
                file.write(response.content)