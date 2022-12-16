import requests, os, csv
from django.core.management.base import BaseCommand, CommandError
from predictionApp.models import *
from competitionApp.models import *
from fixtureApp.models import *
from settings import settings
from dateparser import parse
from coreApp.management.commands.extract_data import get, save_from_file
from datetime import datetime


def function():
    print("-------------------------", datetime.now())

    try:
        url = ['https://www.football-data.co.uk/mmz4281/2223/Latest_Results.csv', "https://www.football-data.co.uk/new/Latest_Results.csv"]
        for i, u in enumerate(url):
            response = requests.get(u)
            with open(os.path.join(settings.BASE_DIR, 'datas/results/data_{}.csv'.format(i)), 'wb') as file:
                file.write(response.content)
        
        
        file = os.path.join(settings.BASE_DIR, "datas/results/data_0.csv")
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
                
                compet             = get(row, header, "Div") or ""
                edicompet= EditionCompetition.objects.filter(competition__code = compet).order_by("-edition__name").first()

                home                    = get(row, header, "HomeTeam") or ""
                away                    = get(row, header, "AwayTeam") or ""
                    
                #enregistrement des équipes
                home, created = EditionTeam.objects.get_or_create(team__name = home, edition = edicompet)
                away, created = EditionTeam.objects.get_or_create(team__name = away, edition = edicompet)
                
                #enregistrement du match et des infos du match
                match, created = Match.objects.get_or_create(
                    date              = parse(get(row, header, "Date") or "", settings={'DATE_ORDER':'DMY', 'TIMEZONE': 'UTC'}),
                    hour              = get(row, header, "Time") or None,
                    home              = home,
                    away              = away,
                    edition           = edicompet,
                    is_finished       = False
                    )
                
                home_score              = get(row, header, "FTHG")
                away_score              = get(row, header, "FTAG")
                result                  = get(row, header, "R") or ""
                home_half_score         = get(row, header, "HTHG")
                away_half_score         = get(row, header, "HTAG")
                result_half             = get(row, header, "HTR") or ""
                
                home_shots              = get(row, header, "HS")
                away_shots              = get(row, header, "AS")
                home_shots_on_target    = get(row, header, "HST")
                away_shots_on_target    = get(row, header, "AST")
                home_fouls              = get(row, header, "HF")
                away_fouls              = get(row, header, "AF")
                home_corners            = get(row, header, "HC")
                away_corners            = get(row, header, "AC")
                home_offsides           = get(row, header, "HO")
                away_offsides           = get(row, header, "AO")
                
                home_yellow_cards       = get(row, header, "HY")
                away_yellow_cards       = get(row, header, "AY")
                home_red_cards          = get(row, header, "HR")
                away_red_cards          = get(row, header, "AR")
                
                
                
                match.home_score        = home_score
                match.away_score        = away_score
                match.result            = result
                match.home_half_score   = home_half_score
                match.away_half_score   = away_half_score
                match.result_half       = result_half
                match.is_finished       = True
                match.save()

                

                extra, created = ExtraInfosMatch.objects.get_or_create(
                    match                   = match,
                    home_shots              = home_shots,
                    away_shots              = away_shots,
                    home_shots_on_target    = home_shots_on_target,
                    away_shots_on_target    = away_shots_on_target,
                    home_corners            = home_corners,
                    away_corners            = away_corners,
                    home_fouls              = home_fouls,
                    away_fouls              = away_fouls,
                    home_offsides           = home_offsides,
                    away_offsides           = away_offsides,
                    home_yellow_cards       = home_yellow_cards,
                    away_yellow_cards       = away_yellow_cards,
                    home_red_cards          = home_red_cards,
                    away_red_cards          = away_red_cards
                    )
                
                
                #enregistrement des cotes
                booker = Bookmaker.objects.get(code = "B365")
                oddsmatch, created = OddsMatch.objects.get_or_create(
                    match = match, 
                    booker = booker,
                    home = float(get(row, header, "Avg H") or 0.0),
                    draw = float(get(row, header, "Avg D") or 0.0),
                    away = float(get(row, header, "Avg A") or 0.0)
                    )
                        
                
                print(match, match.date)
                
    except Exception as e:
        print("Errror 12 --------------------------------", e)
            
            
            
            
            
            
    try:   

        file = os.path.join(settings.BASE_DIR, "datas/results/data_1.csv")
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
                
                compet                = get(row, header, "League") or ""
                pays                  = get(row, header, "Country") or ""
                edicompet  = EditionCompetition.objects.filter(competition__code = compet, competition__pays__name = pays ).order_by("-edition__name").first()
                
                home                    = get(row, header, "Home") or ""
                away                    = get(row, header, "Away") or ""
                    
                #enregistrement des équipes
                home, created = EditionTeam.objects.get_or_create(team__name = home, edition = edicompet)
                away, created = EditionTeam.objects.get_or_create(team__name = away, edition = edicompet)
                
                #enregistrement du match et des infos du match
                match, created = Match.objects.get_or_create(
                    date              = parse(get(row, header, "Date") or "", settings={'DATE_ORDER':'DMY', 'TIMEZONE': 'UTC'}),
                    hour              = get(row, header, "Time") or None,
                    home              = home,
                    away              = away,
                    edition           = edicompet,
                    is_finished       = False
                    )
                
                home_score              = get(row, header, "HG")
                away_score              = get(row, header, "AG")
                result                  = get(row, header, "Res") or ""
                home_half_score         = get(row, header, "HTHG")
                away_half_score         = get(row, header, "HTAG")
                result_half             = get(row, header, "HTR") or ""
                
                home_shots              = get(row, header, "HS")
                away_shots              = get(row, header, "AS")
                home_shots_on_target    = get(row, header, "HST")
                away_shots_on_target    = get(row, header, "AST")
                home_fouls              = get(row, header, "HF")
                away_fouls              = get(row, header, "AF")
                home_corners            = get(row, header, "HC")
                away_corners            = get(row, header, "AC")
                home_offsides           = get(row, header, "HO")
                away_offsides           = get(row, header, "AO")
                
                home_yellow_cards       = get(row, header, "HY")
                away_yellow_cards       = get(row, header, "AY")
                home_red_cards          = get(row, header, "HR")
                away_red_cards          = get(row, header, "AR")
                
                
                match.home_score        = home_score
                match.away_score        = away_score
                match.result            = result
                match.home_half_score   = home_half_score
                match.away_half_score   = away_half_score
                match.result_half       = result_half
                match.is_finished       = True
                match.save()
                
                
                extra, created = ExtraInfosMatch.objects.get_or_create(
                    match                   = match,
                    home_shots              = home_shots,
                    away_shots              = away_shots,
                    home_shots_on_target    = home_shots_on_target,
                    away_shots_on_target    = away_shots_on_target,
                    home_corners            = home_corners,
                    away_corners            = away_corners,
                    home_fouls              = home_fouls,
                    away_fouls              = away_fouls,
                    home_offsides           = home_offsides,
                    away_offsides           = away_offsides,
                    home_yellow_cards       = home_yellow_cards,
                    away_yellow_cards       = away_yellow_cards,
                    home_red_cards          = home_red_cards,
                    away_red_cards          = away_red_cards
                    )
                
                
                #enregistrement des cotes
                booker = Bookmaker.objects.get(code = "B365")
                oddsmatch, created = OddsMatch.objects.get_or_create(
                    match = match, 
                    booker = booker,
                    home = float(get(row, header, "Avg H") or 0.0),
                    draw = float(get(row, header, "Avg D") or 0.0),
                    away = float(get(row, header, "Avg A") or 0.0)
                    )
                
                
                print(match, match.date)
                
    except Exception as e:
        print("Errror 44 --------------------------------", e)
                