import requests
from django.core.management.base import BaseCommand, CommandError
from prediction.models import *
from features.models import *
from dateparser import parse

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        url = ['https://www.football-data.co.uk/fixtures.csv', "https://www.football-data.co.uk/new_league_fixtures.csv"]
        for i, u in enumerate(url):
            response = requests.get(u)
            with open('datas/fixtures/data_{}.csv'.format(i), 'wb') as file:
                file.write(response.content)