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


def get(datas, header, key):
    try:
        index = indexof(header, key)
        if index >= 0:
            if index > len(datas):
                return None
            return datas[index].lstrip() or None
        return None
    except:
        return None


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
        contries = sorted(contries)
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
                                
                                
                                home                    = get(row, header, "HomeTeam") or ""
                                away                    = get(row, header, "AwayTeam") or ""
                                home_score              = get(row, header, "FTHG")
                                away_score              = get(row, header, "FTAG")
                                result                  = get(row, header, "FTR") or ""
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
    
                                #enregistrement des équipes
                                team, created = Team.objects.get_or_create(name = home, pays = pays)
                                home, created = EditionTeam.objects.get_or_create(team = team, edition = edicompet)
                                
                                team, created = Team.objects.get_or_create(name = away, pays = pays)
                                away, created = EditionTeam.objects.get_or_create(team = team, edition = edicompet)
                                
                                #enregistrement du match et des infos du match
                                match, created = Match.objects.get_or_create(
                                    date              = parse(get(row, header, "Date") or "", settings={'DATE_ORDER':'DMY', 'TIMEZONE': 'UTC'}),
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
                                            home = float(get(row, header, code+"H") or 0.0),
                                            draw = float(get(row, header, code+"D") or 0.0),
                                            away = float(get(row, header, code+"A") or 0.0)
                                            )
                                      
                              
                                print(competition_, edition_, match.date)


        self.stdout.write(self.style.SUCCESS('Successful !'))
        
        
        
        
