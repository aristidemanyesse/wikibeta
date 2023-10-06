from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta, date
from competitionApp.models import *
from django.db.models import Avg, Sum, Count
import pytz, threading, time, os
from settings.settings import MEDIA_ROOT

utc=pytz.UTC

def function( date = None):
    date = datetime.now().replace(tzinfo=utc).date() if date is None else date
    print("Ranking pour le -------------------------", date)
    try :
        for edition in EditionCompetition.objects.filter(start_date__lte = date, finish_date__gte = date).order_by("-edition__name"):
            last = edition.edition_rankings.filter(date__range = [date - timedelta(days = 1), date+ timedelta(days = 1)], deleted = False).count()
            
            if last == 0:
                print("Ranking de --", edition)
                rank = Ranking.objects.create(
                    edition = edition,
                    date = date
                )
                
                datas = edition.classement(date)
                for i, line in enumerate(datas):
                    LigneRanking.objects.create(
                        ranking   = rank,
                        team      = line["team"],
                        level     = i+1,
                        mj        = line["mj"],
                        win       = line["win"],
                        draw      = line["draw"],
                        lose      = line["lose"],
                        gs        = line["gs"],
                        ga        = line["ga"],
                        gd        = line["gd"],
                        form      = line["form"],
                        pts       = line["pts"],
                        ppg       = line["ppg"],
                        cs        = line["cs"],
                        btts      = line["btts"],
                        avg_gs    = line["avg_gs"],
                        avg_ga    = line["avg_ga"],
                        p1_5      = line["p1_5"],
                        p2_5      = line["p2_5"],
                        m3_5      = line["m3_5"],
                    )
                
                
                extra = ExtraInfosMatch.objects.filter(match__is_finished = True, match__edition = edition, match__date__lt = date).aggregate(
                    Avg("home_shots"), Avg("away_shots"), 
                    Avg("home_shots_on_target"), Avg("away_shots_on_target"),
                    Avg("home_corners"), Avg("away_corners"), 
                    Avg("home_fouls"), Avg("away_fouls"),
                    Avg("home_offsides"), Avg("away_offsides"),
                    Avg("home_yellow_cards"), Avg("away_yellow_cards"),
                    Avg("home_red_cards"), Avg("away_red_cards")
                )
                
    
                result = ResultMatch.objects.filter(match__is_finished = True, match__edition = edition, match__date__lt = date).aggregate(
                    Avg("home_score"), Avg("away_score"),
                )
                CompetitionStat.objects.create(
                    edition             = edition,
                    ranking             = rank,
                    avg_goals           = round(result["home_score__avg"] or 0, 2) + round(result["away_score__avg"] or 0, 2),
                    avg_fouls           = round(extra["home_fouls__avg"] or 0, 2) + round(extra["away_fouls__avg"] or 0, 2),
                    avg_corners         = round(extra["home_corners__avg"] or 0, 2) + round(extra["away_corners__avg"] or 0, 2),
                    avg_shots           = round(extra["home_shots__avg"] or 0, 2) + round(extra["away_shots__avg"] or 0, 2),
                    avg_shots_target    = round(extra["home_shots_on_target__avg"] or 0, 2) + round(extra["away_shots_on_target__avg"] or 0, 2),
                    avg_offside         = round(extra["home_offsides__avg"] or 0, 2) + round(extra["away_offsides__avg"] or 0, 2),
                    avg_yellow_cards    = round(extra["home_yellow_cards__avg"] or 0, 2) + round(extra["away_yellow_cards__avg"] or 0, 2),
                    avg_red_cards       = round(extra["home_red_cards__avg"] or 0, 2) + round(extra["away_red_cards__avg"] or 0, 2),
                )

    
    except Exception as e:
        print("Error ", e)
        
        
        

def handle(): 
    print("--------------------------------", datetime.now())  
    with open(os.path.join(MEDIA_ROOT, "date_ranking.txt"), "r+") as file:
        date_string = file.read()
        mydate = datetime.strptime(date_string, '%Y-%m-%d').date() if date_string else datetime(1993,7,23)
        
        if mydate < datetime.now().date():
            while threading.active_count() > 50:
                time.sleep(200)

            p = threading.Thread(target=function, args=(mydate,))
            p.setDaemon(True)
            p.start()
            time.sleep(0.5)
            
            mydate += timedelta(days=3)
            file.seek(0)  # Se positionner au début du fichier pour écrire
            file.write(mydate.strftime('%Y-%m-%d'))
            file.truncate()
            
            while threading.active_count() > 1:
                print("en attente ---------------: ", threading.active_count())
                time.sleep(30)
            
        

            