from django.core.management.base import BaseCommand, CommandError
from bettingApp.models import *
from fixtureApp.models import *
from statsApp.models import *
from competitionApp.models import *
from predictionApp.models import *
from dateparser import parse
import threading, time, requests
from .headers import * 
from .tools import * 
from datetime import datetime, timedelta
    

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://footapi7.p.rapidapi.com/api/matches/{}/{}/{}".format(day, month, year)
        datas = requests.request("GET", url, headers=ARISTIDEMANYESSE).json()
        
        matchs = Match.objects.all()
        
        for event in datas["events"]:
            event["status"]
            event["awayTeam"]
            event["awayScore"]
            event["homeTeam"]
            event["homeScore"]
            test = False
            for pay in pays:
                if similar(pay.name, country["name"]) > 0.9:
                    pay.code = country["id"]
                    pay.abr = country["alpha2"]
                    pay.save()
                    break
                
            if not test:
                Pays.objects.create(
                    code=country["id"], 
                    name = country["name"],
                    abr = country["alpha2"]
                )