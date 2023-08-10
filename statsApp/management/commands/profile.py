from django.core.management.base import BaseCommand, CommandError
from bettingApp.models import *
from coreApp.templatetags import footstats
from fixtureApp.models import *
from statsApp.models import *
from competitionApp.models import *
from predictionApp.models import *
from dateparser import parse
import threading
import time,pytz
from datetime import datetime, timedelta
    

class Command(BaseCommand):


    def handle(self, *args, **options):
        for match in Match.objects.filter(is_finished=False):
            extra_infos = match.get_extra_info_match()
            print(match)
            
            for team in [match.home, match.away]:
                
                matches = team.get_last_matchs(match, number = 10, edition = True)
                rank = LigneRanking.objects.filter(team = team, ranking__date__lte = match.date).order_by('-ranking__date').first()
                
                if rank is None:
                    print("**************")
                    continue
                
                # DYNAMIQ
                win, vn, buts, enc, mibuts = 0, 0, 0, 0, 0
                for x in matches[:5]:
                    result = x.get_result()
                    if result is not None:
                        if result.result == "H":
                            win += 1 if (x.home == team) else 0
                        elif result.result == "A":
                            win += 1 if (x.away == team) else 0
                            
                for x in matches:
                    result = x.get_result()
                    if result is not None:
                        buts += 1 if ((result.home_score > 0 and team == x.home) or (result.away_score > 0 and team == x.away)) else 0
                        enc += 1 if ((result.home_score > 0 and team == x.away) or (result.away_score > 0 and team == x.home)) else 0
                        if result.home_half_score is not None:
                            mibuts += 1 if ((result.home_half_score > 0 and team == x.home) or (result.away_half_score > 0 and team == x.away)) else 0
                        if result.result == "D":
                            vn += 1
                        elif result.result == "H":
                            vn += 1 if (x.home == team) else 0
                        elif result.result == "A":
                            vn += 1 if (x.away == team) else 0
                            
                
                dynamic = win + (vn * 0.5 )+ (5 - round(rank.level / 4)+1)
                
                
                #ATK
                attack = (rank.avg_gs * 1.5)  + (buts * 0.5) +1.5
                target = 0
                if extra_infos is not None:
                    target = extra_infos.home_shots_on_target if (x.home == team) else extra_infos.away_shots_on_target 
                    attack += -1.5 + (target or 0 / 1.5)
                
                
                #DEF
                defense = (5 - rank.avg_ga) + (5 - (enc * 0.5)) + 1.5
                fautes = 0
                if extra_infos is not None:
                    fautes = extra_infos.home_fouls if (x.home == team) else extra_infos.away_fouls
                    defense += -1.5 + (5 - ((fautes or 0)/ 3))
                
                
                #PRESSION
                tirs, corners = 0, 0
                if extra_infos is not None:
                    tirs = extra_infos.home_shots if (x.home == team) else extra_infos.away_shots                    
                    corners = extra_infos.home_corners if (x.home == team) else extra_infos.away_corners                    
                pression = ((corners or 0) / 2) + ((tirs or 0 )/ 3) + (mibuts * 0.5)
                
                
                #CLEANING
                if extra_infos is None:
                    clean = 0
                else:
                    cartons, offsides = 0, 0
                    cartons = extra_infos.home_yellow_cards or 0 + (extra_infos.home_red_cards or 0 * 2) if (x.home == team) else extra_infos.away_yellow_cards or 0 + (extra_infos.away_red_cards or 0 * 2)                
                    offsides = extra_infos.home_offsides  if (x.home == team) else extra_infos.away_offsides                
                    clean = (5 - (offsides or 0)) + ( 5 - ((fautes or 0) / 3)) + (5 - (cartons or 0))
                
                utc=pytz.UTC
                date = datetime.now().replace(tzinfo=utc)
                TeamProfileMatch.objects.create(date = date, team=team, match=match, dynamic=dynamic, pression= pression, attack = attack, defense=defense, clean=clean)
                
                
                
        

  