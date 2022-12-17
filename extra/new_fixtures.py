import requests, os, csv
from django.core.management.base import BaseCommand, CommandError
from predictionApp.models import *
from settings import settings
from competitionApp.models import *
from fixtureApp.models import *
from dateparser import parse
from coreApp.management.commands.extract_data import get, save_from_file
from datetime import datetime


def function():
    print("-------------------------", datetime.now())
    try:
        url = ['https://www.football-data.co.uk/fixtures.csv', "https://www.football-data.co.uk/new_league_fixtures.csv"]
        for i, u in enumerate(url):
            response = requests.get(u)
            with open(os.path.join(settings.BASE_DIR, 'datas/fixtures/data_{}.csv'.format(i)), 'wb') as file:
                file.write(response.content)
        
        file = os.path.join(settings.BASE_DIR, "datas/fixtures/data_0.csv")
        with open(file ,'rt', encoding = 'ISO-8859-1') as f:
            data = csv.reader(f)
            i = 0
            for row in data:
                if i == 0:
                    header = row
                    i = 1
                    continue
                
                #si c'est une ligne vide
                if len(row) < 2:
                    continue
                
                compet    = get(row, header, "Div") or ""
                if compet != "":
                    edicompet = EditionCompetition.objects.filter(competition__code = compet).order_by("-edition__name").first()

                    home      = get(row, header, "HomeTeam") or ""
                    away      = get(row, header, "AwayTeam") or ""
                        
                    #enregistrement des équipes
                    home, created = Team.objects.get_or_create(name = home, pays = edicompet.competition.pays )
                    home, created = EditionTeam.objects.get_or_create(team = home, edition = edicompet)
                    
                    away, created = Team.objects.get_or_create(name = away, pays = edicompet.competition.pays )
                    away, created = EditionTeam.objects.get_or_create(team = away, edition = edicompet)
                    
                    #enregistrement du match et des infos du match
                    match, created = Match.objects.get_or_create(
                        date              = parse(get(row, header, "Date") or "", settings={'DATE_ORDER':'DMY', 'TIMEZONE': 'UTC'}),
                        hour              = get(row, header, "Time") or None,
                        home              = home,
                        away              = away,
                        edition           = edicompet
                        )
                    
                    print("resultat 1 pour ", match)
    except Exception as e:
        print("Errror 12 --------------------------------", e)



    try:
        file = os.path.join(settings.BASE_DIR, "datas/fixtures/data_1.csv")
        with open(file ,'rt', encoding = 'ISO-8859-1') as f:
            data = csv.reader(f)
            i = 0
            for row in data:
                if i == 0:
                    header = row
                    i = 1
                    continue
                
                #si c'est une ligne vide
                if len(row) < 2:
                    continue
                
                compet    = get(row, header, "League") or ""
                pays      = get(row, header, "Country") or ""
                
                if compet != "" and pays != "" :
                    pays, created = Pays.objects.get_or_create(name = pays)
                    compet, created = Competition.objects.get_or_create(code = compet, pays = pays)
                    
                    edicompet = EditionCompetition.objects.filter(competition = compet).order_by("-edition__name").first()
                    if edicompet is not None:
                        if edicompet.is_finished :
                            edicompet = EditionCompetition.objects.create(competition = compet, edition = Edition.objects.create(name = edicompet.edition.next()))
                    else:
                        edit, created = Edition.objects.get_or_create(name = "{}-{}".format(datetime.now().year, datetime.now().year+1))
                        edicompet = EditionCompetition.objects.create(competition = compet, edition = edit)


                    home      = get(row, header, "Home") or ""
                    away      = get(row, header, "Away") or ""
                        
                    #enregistrement des équipes
                    home, created = Team.objects.get_or_create(name = home, pays = pays )
                    home, created = EditionTeam.objects.get_or_create(team = home, edition = edicompet)
                    
                    away, created = Team.objects.get_or_create(name = away, pays = pays )
                    away, created = EditionTeam.objects.get_or_create(team = away, edition = edicompet)

                    #enregistrement du match et des infos du match
                    match, created = Match.objects.get_or_create(
                        date              = parse(get(row, header, "Date") or "", settings={'DATE_ORDER':'DMY', 'TIMEZONE': 'UTC'}),
                        hour              = get(row, header, "Time") or None,
                        home              = home,
                        away              = away,
                        edition           = edicompet
                        )
                    print("Resultat 2 pour ", match)
    except Exception as e:
        print("Errror 7887 --------------------------------", e)                