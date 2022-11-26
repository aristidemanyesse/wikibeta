from django.core.management.base import BaseCommand, CommandError
import csv, os, re
from betting.models import *
from features.models import *
from dateparser import parse


def indexof(list, str):
    try:
        return list.index(str)
    except :
        return -1


def booker_listed(booker:Bookmaker , row:list):
    return  booker.code+"H" in row and booker.code+"D" in row and booker.code+"A" in row
   

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        
        ## FOR ALL BOOKMAKERS ##
        with open("datas/bookmakers.txt",'rt', encoding='utf-8' ) as file:
            for line in file:
                code, name = line.split(" = ")
                name = name.replace("home win odds", "").replace("draw odds", "").replace("away win odds", "")
                #enregistrement des editions
                booker, created = Bookmaker.objects.get_or_create(name = name.capitalize(), code = code[:-1])
        
        
        
        
        ## FOR ALL MATCHES ##
        contries = [x for x in os.listdir("datas/lot1/") if os.path.isdir("datas/lot1/{}".format(x))]
        for contry in contries:
            #enregistrement des pays
            pays, created = Pays.objects.get_or_create(name = contry.capitalize())
            editions = [x for x in os.listdir("datas/lot1/{}".format(contry)) if os.path.isdir("datas/lot1/{}/{}".format(contry, x))]
            
            for edition in editions:
                #enregistrement des editions
                edition_, created = Edition.objects.get_or_create(name = edition)
                competitions = [x for x in os.listdir("datas/lot1/{}/{}/".format(contry, edition)) if not os.path.isdir("datas/lot1/{}/{}/{}".format(contry, edition, x))]
                
                for compet in competitions:
                    path = "datas/lot1/{}/{}/{}".format(contry, edition, compet)
                    
                    if os.path.exists(path):
                        #enregistrement des competitions
                        compet = compet.split(".")[0]
                        competition_, created = Competition.objects.get_or_create(name = compet, pays = pays)
                        edicompet, created = EditionCompetition.objects.get_or_create(edition = edition_, competition = competition_)
                        
                        print("----------------", path)
                        with open(path,'rt', encoding = 'ISO-8859-1') as f:
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
                                
                                home                    = row[indexof(header, "HomeTeam")].lstrip() if indexof(header, "HomeTeam") >= 0 else ""
                                away                    = row[indexof(header, "AwayTeam")].lstrip() if indexof(header, "AwayTeam") >= 0 else ""
                                home_score              = (row[indexof(header, "FTHG")].lstrip() if indexof(header, "FTHG") >= 0 else None) or None
                                away_score              = (row[indexof(header, "FTAG")].lstrip() if indexof(header, "FTAG") >= 0 else None) or None
                                result                  = row[indexof(header, "FTR")].lstrip() if indexof(header, "FTR") >= 0 else ""
                                home_half_score         = (row[indexof(header, "HTHG")].lstrip() if indexof(header, "HTHG") >= 0 else None) or None
                                away_half_score         = (row[indexof(header, "HTAG")].lstrip() if indexof(header, "HTAG") >= 0 else None) or None
                                result_half             = row[indexof(header, "HTR")].lstrip() if indexof(header, "HTR") >= 0 else ""
                                
                                home_shots              = (row[indexof(header, "HS")].lstrip() if indexof(header, "HS") >= 0 else None) or None
                                away_shots              = (row[indexof(header, "AS")].lstrip() if indexof(header, "AS") >= 0 else None) or None
                                home_shots_on_target    = (row[indexof(header, "HST")].lstrip() if indexof(header, "HST") >= 0 else None) or None
                                away_shots_on_target    = (row[indexof(header, "AST")].lstrip() if indexof(header, "AST") >= 0 else None) or None
                                home_fouls              = (row[indexof(header, "HF")].lstrip() if indexof(header, "HF") >= 0 else None) or None
                                away_fouls              = (row[indexof(header, "AF")].lstrip() if indexof(header, "AF") >= 0 else None) or None
                                home_corners            = (row[indexof(header, "HC")].lstrip() if indexof(header, "HC") >= 0 else None) or None
                                away_corners            = (row[indexof(header, "AC")].lstrip() if indexof(header, "AC") >= 0 else None) or None
                                home_offsides           = (row[indexof(header, "HO")].lstrip() if indexof(header, "HO") >= 0 else None) or None
                                away_offsides           = (row[indexof(header, "AO")].lstrip() if indexof(header, "AO") >= 0 else None) or None
                                
                                home_yellow_cards       = (row[indexof(header, "HY")].lstrip() if indexof(header, "HY") >= 0 else None) or None
                                away_yellow_cards       = (row[indexof(header, "AY")].lstrip() if indexof(header, "AY") >= 0 else None) or None
                                home_red_cards          = (row[indexof(header, "HR")].lstrip() if indexof(header, "HR") >= 0 else None) or None
                                away_red_cards          = (row[indexof(header, "AR")].lstrip() if indexof(header, "AR") >= 0 else None) or None
    
                                #enregistrement des équipes
                                team, created = Team.objects.get_or_create(name = home, pays = pays)
                                home, created = EditionTeam.objects.get_or_create(team = team, edition = edicompet)
                                
                                team, created = Team.objects.get_or_create(name = away, pays = pays)
                                away, created = EditionTeam.objects.get_or_create(team = team, edition = edicompet)
                                
                                #enregistrement du match et des infos du match
                                match, created = Match.objects.get_or_create(
                                    date              = parse(row[indexof(header, "Date")].lstrip() if indexof(header, "Date") >= 0 else None, settings={'TIMEZONE': 'UTC'}),
                                    home              = home,
                                    away              = away,
                                    edition           = edicompet,
                                    home_score        = home_score,
                                    away_score        = away_score,
                                    result            = result,
                                    home_half_score   = home_half_score,
                                    away_half_score   = away_half_score,
                                    result_half       = result_half
                                    )
                                
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
                                for booker in Bookmaker.objects.all():
                                    if booker_listed(booker, header):
                                        code = booker.code
                                        oddsmatch, created = OddsMatch.objects.get_or_create(
                                            match = match, 
                                            booker = booker,
                                            home = (row[indexof(header, code+"H")].lstrip() if indexof(header, code+"H") >= 0 else 1) or None,
                                            draw = (row[indexof(header, code+"D")].lstrip() if indexof(header, code+"D") >= 0 else 1) or None,
                                            away = (row[indexof(header, code+"A")].lstrip() if indexof(header, code+"A") >= 0 else 1) or None,
                                            )
                                      
                              
                                print(competition_, edition_, match.date)


        self.stdout.write(self.style.SUCCESS('Successful !'))