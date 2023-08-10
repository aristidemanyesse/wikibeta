import requests, os, csv, time, pytz
from django.core.management.base import BaseCommand, CommandError
from predictionApp.models import *
from competitionApp.models import *
from fixtureApp.models import *
from settings import settings
from dateparser import parse
from coreApp.management.commands.extract_data import get, save_from_file
from datetime import datetime


utc=pytz.UTC

def function2( date = None):
    
    date = datetime.now().replace(tzinfo=utc) if date is None else date
    print("Ranking pour le -------------------------", date)
    try :
        for edition in EditionCompetition.objects.filter(start_date__lte = date.date(), finish_date__gte = date.date()).order_by("-edition__name"):
            last = edition.edition_rankings.filter(date__range = [date.date() - timedelta(days = 1), date.date()+ timedelta(days = 1)]).count()
            
            if last == 0:
                print("Ranking de --", edition)
                rank = Ranking.objects.create(
                    edition = edition,
                    date = date
                )
                
                datas = edition.classement(date.date())
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
                
                # matchs = edition.edition_du_match.filter(is_finished = True)
                # corners = fouls = shots = shots_on_target = offsides = yellow_cards = red_cards = 0
                                
                # extra = ExtraInfosMatch.objects.filter(match__is_finished = True, match__edition = edition, match__date__lte = date).aggregate(
                #     Avg("home_shots"), Avg("away_shots"), 
                #     Avg("home_shots_on_target"), Avg("away_shots_on_target"),
                #     Avg("home_corners"), Avg("away_corners"), 
                #     Avg("home_fouls"), Avg("away_fouls"),
                #     Avg("home_offsides"), Avg("away_offsides"),
                #     Avg("home_yellow_cards"), Avg("away_yellow_cards"),
                #     Avg("home_red_cards"), Avg("away_red_cards")
                # )
                
                # result = ResultMatch.objects.filter(match__is_finished = True, match__edition = edition, match__date__lte = date).aggregate(
                #     Avg("home_score"), Avg("away_score"),
                # )
                

                # CompetitionStat.objects.create(
                #     edition             = edition,
                #     ranking             = rank,
                #     avg_goals           = round(result["home_score__avg"] or 0, 2) + round(result["away_score__avg"] or 0, 2),
                #     avg_fouls           = round(extra["home_fouls__avg"] or 0, 2) + round(extra["away_fouls__avg"] or 0, 2),
                #     avg_corners         = round(extra["home_corners__avg"] or 0, 2) + round(extra["away_corners__avg"] or 0, 2),
                #     avg_shots           = round(extra["home_shots__avg"] or 0, 2) + round(extra["away_shots__avg"] or 0, 2),
                #     avg_shots_target    = round(extra["home_shots_on_target__avg"] or 0, 2) + round(extra["away_shots_on_target__avg"] or 0, 2),
                #     avg_offside         = round(extra["home_offsides__avg"] or 0, 2) + round(extra["away_offsides__avg"] or 0, 2),
                #     avg_yellow_cards    = round(extra["home_yellow_cards__avg"] or 0, 2) + round(extra["away_yellow_cards__avg"] or 0, 2),
                #     avg_red_cards       = round(extra["home_red_cards__avg"] or 0, 2) + round(extra["away_red_cards__avg"] or 0, 2),
                # )
                
                
                # matchs = edition.edition_du_match.filter(is_finished = True).exclude(is_posted = True)
                # teams = edition.edition_team.filter()
                # if len(matchs) == len(teams) * ( len(teams) -1):
                #     edition.is_finished = True
                #     edition.save()

    
    except Exception as e:
        print("Error ", e)
