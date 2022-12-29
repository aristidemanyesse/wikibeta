from django.core.management.base import BaseCommand, CommandError
import csv, os, re
from bettingApp.models import *
from fixtureApp.models import *
from competitionApp.models import *
from dateparser import parse

countries = {
    "B1":"Belgium",
    "D1":"Dustchland",
    "D2":"Dustchland",
    "E0":"England",
    "E1":"England",
    "E2":"England",
    "E3":"England",
    "EC":"England",
    "F1":"France",
    "F2":"France",
    "G1":"Greece",
    "I1":"Italia",
    "I2":"Italia",
    "N1":"Norway",
    "P1":"Portugal",
    "SC0":"Scotland",
    "SC1":"Scotland",
    "SC2":"Scotland",
    "SC3":"Scotland",
    "SP1":"Spain",
    "SP2":"Spain",
    "T1":"Turkey"
}
        
        
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








def save_from_dir(path):
    if not os.path.exists(path):
        raise Exception("Ce fichier n'existe pas !")
    
    print("Execution du fichier "+path)
    file = path.split("/")[-1]
    edition = path.split("/")[-2]
    edition_, created = Edition.objects.get_or_create(name = edition)
    
    country = countries.get(file.split(".")[0], None)
    if country is not None :
        #enregistrement des pays
        pays, created = Pays.objects.get_or_create(name = country.capitalize())
    
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
                
                compet             = get(row, header, "Div") or ""
                if compet != "":
                    competition_, created = Competition.objects.get_or_create(name = compet, code = compet, pays = pays)
                    edicompet, created = EditionCompetition.objects.get_or_create(edition = edition_, competition = competition_)
            
                    
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

                    if home == "" or away == "":
                        continue
                    #enregistrement des équipes
                    team, created = Team.objects.get_or_create(name = home, pays = pays)
                    home, created = EditionTeam.objects.get_or_create(team = team, edition = edicompet)
                    
                    team, created = Team.objects.get_or_create(name = away, pays = pays)
                    away, created = EditionTeam.objects.get_or_create(team = team, edition = edicompet)
                    
                    #enregistrement du match et des infos du match
                    match, created = Match.objects.get_or_create(
                        date              = parse(get(row, header, "Date") or "", settings={'DATE_ORDER':'DMY', 'TIMEZONE': 'UTC'}),
                        hour              = get(row, header, "Time") or None,
                        home              = home,
                        away              = away,
                        edition           = edicompet,
                        is_finished       = True
                        )
                    
                    if created:
                        info, created = ResultMatch.objects.get_or_create(
                            match             = match,
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
                                if get(row, header, code+"H") == "" or get(row, header, code+"H") == 0 or get(row, header, code+"H") is None:
                                    continue
                                oddsmatch, created = OddsMatch.objects.get_or_create(
                                    match = match, 
                                    booker = booker,
                                    home = float(get(row, header, code+"H")),
                                    draw = float(get(row, header, code+"D")),
                                    away = float(get(row, header, code+"A"))
                                    )
                                










def save_from_file(path):
    if not os.path.exists(path):
        raise Exception("Ce fichier n'existe pas !")
    
    print("Execution du fichier "+path)
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
            
            pa = get(row, header, "Country") or ""
            pays, created = Pays.objects.get_or_create(name = pa.capitalize())
    
            edition = get(row, header, "Season")
            if len(edition) > 8:
                edition = "{}-{}".format(edition.split("/")[0], edition.split("/")[1])
                
            if edition == "" or edition is None:
                continue
            edition_, created = Edition.objects.get_or_create(name = edition)
            
            compet             = get(row, header, "League") or ""
            if compet != "":
                competition_, created = Competition.objects.get_or_create(name = compet, code = compet, pays = pays)
                edicompet, created = EditionCompetition.objects.get_or_create(edition = edition_, competition = competition_)
        
                
                home                    = get(row, header, "Home") or ""
                away                    = get(row, header, "Away") or ""
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

                if home == "" or away == "":
                    continue
                #enregistrement des équipes
                team, created = Team.objects.get_or_create(name = home, pays = pays)
                home, created = EditionTeam.objects.get_or_create(team = team, edition = edicompet)
                
                team, created = Team.objects.get_or_create(name = away, pays = pays)
                away, created = EditionTeam.objects.get_or_create(team = team, edition = edicompet)
                
                #enregistrement du match et des infos du match
                match, created = Match.objects.get_or_create(
                    date              = parse(get(row, header, "Date") or "", settings={'DATE_ORDER':'DMY', 'TIMEZONE': 'UTC'}),
                    hour              = get(row, header, "Time") or None,
                    home              = home,
                    away              = away,
                    edition           = edicompet,
                    is_finished       = True
                    )
                
                if created:
                    info, created = ResultMatch.objects.get_or_create(
                        match             = match,
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
                            if get(row, header, code+"H") == "" or get(row, header, code+"H") == 0 or get(row, header, code+"H") is None:
                                continue
                            oddsmatch, created = OddsMatch.objects.get_or_create(
                                match = match, 
                                booker = booker,
                                home = float(get(row, header, code+"H")),
                                draw = float(get(row, header, code+"D")),
                                away = float(get(row, header, code+"A"))
                                )
                            

