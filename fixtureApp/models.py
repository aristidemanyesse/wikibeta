from django.db import models
from django.db.models import Avg, Sum, Q
from annoying.decorators import signals
from coreApp.models import BaseModel
from coreApp.functions import *
from statsApp.models import *
from bettingApp.models import *
from datetime import datetime, timedelta, time

import statsApp.get_home_facts as get_home_facts
import statsApp.get_away_facts as get_away_facts

from coreApp.management.crons.before_stats_match import function as before_stats_match

def intersection(list1, list2):
    return [value for value in list1 if value in list2]

    
class Match(BaseModel):
    date           = models.DateField( null = True, blank=True)
    hour           = models.TimeField( null = True, blank=True)
    home           = models.ForeignKey("teamApp.EditionTeam", on_delete = models.CASCADE, related_name="home_match")
    away           = models.ForeignKey("teamApp.EditionTeam", on_delete = models.CASCADE, related_name="away_match")
    edition        = models.ForeignKey("competitionApp.EditionCompetition", on_delete = models.CASCADE, related_name="edition_du_match")
    is_finished    = models.BooleanField(default = False, null = True, blank=True)
    is_posted      = models.BooleanField(default = False)
    is_first_match = models.BooleanField(default = False, null = True, blank=True)
    is_predict     = models.BooleanField(default = False, null = True, blank=True)
    is_compared    = models.BooleanField(default = False, null = True, blank=True)
    is_facted      = models.BooleanField(default = False, null = True, blank=True)
    is_stated      = models.BooleanField(default = False, null = True, blank=True)

    class Meta:
        ordering = ['date', "hour", "home"]
    
    
    def __str__(self):
        return str(self.home) +" -VS- "+ str(self.away)


    def get_result(self):
        return self.result_match.filter().first()
       
       
    
    def confrontations_directes(self, number = 50):
        matchs = Match.objects.filter(Q(home__team = self.home.team, away__team = self.away.team) | Q(home__team = self.away.team,  away__team = self.home.team)).filter(date__lt = self.date, is_finished = True).exclude(id = self.id).order_by("-date")        
        return matchs[:number]
    
    
    def similaires_ppg(self, number = 100):
        try:
            matchs = []
            date = self.date - timedelta(days = 5 * 12 * 30)
            home = self.get_home_before_stats()
            away = self.get_away_before_stats()
            if home is not None:
                ppg_home = home.ppg
                ppg_away = away.ppg
                befores = BeforeMatchStat.objects.filter(match__is_finished = True, ppg__range = intervale(ppg_home), match__edition__competition = self.edition.competition, match__date__range = [date, self.date - timedelta(days = 1)]).exclude(id = home.id).order_by("-match__date")
                for bef in befores:
                    if bef.team == bef.match.home:
                        pa = bef.match.before_stat_match.exclude(id = bef.id).first()
                        if intervale(ppg_away)[0] <= pa.ppg <= intervale(ppg_away)[1] :
                            if bef.match not in matchs:
                                matchs.append(bef.match)
                                
        except Exception as e:
            print("Error similaires_ppg ********", e)
                
        return matchs[:number]




    def similaires_ppg2(self, number = 100):
        try:
            matchs = []
            date = self.date - timedelta(days = 5 * 12 * 30)
            home = self.get_home_before_stats()
            away = self.get_away_before_stats()
            if home is not None:
                ppg_home = home.ppg
                ppg_away = away.ppg
                befores = BeforeMatchStat.objects.filter( match__is_finished = True, ppg__range = intervale2(ppg_home), match__edition__competition = self.edition.competition, match__date__range = [date, self.date - timedelta(days = 1)]).exclude(id = home.id).order_by("-match__date")
                for bef in befores:
                    if bef.team == bef.match.home:
                        pa = bef.match.before_stat_match.exclude(id = bef.id).first()
                        if intervale2(ppg_away)[0] <= pa.ppg <= intervale2(ppg_away)[1] :
                            if bef.match not in matchs:
                                matchs.append(bef.match)
                                
        except Exception as e:
            print("Error similaires_ppg2 ********", e)
            
        return matchs[:number]

        
        

    def similaires_betting(self, number = 100):
        matchs = []
        actual = self.get_odds()
        if actual is not None:
            date = self.date - timedelta(days = 5 * 12 * 30)
            odds = OddsMatch.objects.filter(match__is_finished = True, home__range = intervale(actual.home), match__edition__competition = self.edition.competition, match__date__lt = self.date, match__date__gte = date).exclude(id = self.id).order_by("-match__date")
            for odd in odds:
                if intervale(odd.home) == intervale(actual.home):
                    befs = OddsMatch.objects.filter(away__range = intervale(actual.away), match = odd.match).exclude(id = odd.id)
                    if len(befs) == 1 and odd.match not in matchs:
                        matchs.append(odd.match)
        return matchs[:number]
        
        
    def similaires_intercepts(self, number = 10):
        return intersection(self.similaires_ppg2(), self.similaires_betting())[:number]
    
    
    
    def get_home_before_stats(self):
        return self.home.get_before_stats(self)
    
    
    def get_away_before_stats(self):
        return self.away.get_before_stats(self)
    

    def get_odds(self):
        return self.match_odds.filter().first()
    

    def get_extra_info_match(self):
        return self.extra_info_match.filter().first()
    
    



    
class Goal(BaseModel):
    match             = models.ForeignKey("fixtureApp.Match", on_delete = models.CASCADE, related_name="goal_du_match")
    team              = models.ForeignKey("teamApp.Team", on_delete = models.CASCADE, related_name="team_du_goal")
    minute            = models.CharField(max_length = 255, null = True, blank=True)
    is_penalty        = models.BooleanField(default = False, null = True, blank=True)
    home_half_score   = models.IntegerField(default = 0, null = True, blank=True)
    away_half_score   = models.IntegerField(default = 0, null = True, blank=True)

    def __str__(self):
        return str(self.team) +" goal in "+ str(self.match)






#=====================================================================================================================================================================================
# SIGNAUX --- SIGNAUX ---SIGNAUX --- SIGNAUX ---SIGNAUX --- SIGNAUX ---SIGNAUX --- SIGNAUX ---SIGNAUX --- SIGNAUX ---SIGNAUX --- SIGNAUX ---SIGNAUX --- SIGNAUX ---SIGNAUX --- SIGNAUX
#=====================================================================================================================================================================================





# connect to registered signal
@signals.post_save(sender=Match)
def sighandler(instance, created, **kwargs):
    try:
        #creation du before stat pour chaque equipe
        if created:
            edition = instance.edition
            matchs = edition.edition_du_match.filter(deleted = False).order_by("date").exclude(date = None)
            if  matchs.first() is not None and matchs.last() is not None:
                edition.start_date =   matchs.first().date  
                edition.finish_date =   matchs.last().date  
                edition.save()
                
                
            for team in [instance.home, instance.away]:
                pts, ppg, scored, avg_goals_scored, conceded, avg_goals_conceded = team.last_stats(instance, edition = True)
                datas = team.extra_info_stats(instance, edition = True)      
                
                BeforeMatchStat.objects.create(
                    match                       = instance,
                    team                        = instance.home if (instance.home == team) else instance.away,
                    ppg                         = ppg,
                    goals_scored                = scored,
                    avg_goals_scored            = avg_goals_scored,
                    goals_conceded              = conceded,
                    avg_goals_conceded          = avg_goals_conceded,
                    avg_fouls_for               = datas.get("avg_fouls_for", 0),
                    avg_fouls_against           = datas.get("avg_fouls_against", 0),
                    avg_corners_for             = datas.get("avg_corners_for", 0),
                    avg_corners_against         = datas.get("avg_corners_against", 0),
                    avg_shots_for               = datas.get("avg_shots_for", 0),
                    avg_shots_against           = datas.get("avg_shots_against", 0),
                    avg_shots_target_for        = datas.get("avg_shots_target_for", 0),
                    avg_shots_target_against    = datas.get("avg_shots_target_against", 0),
                    avg_offside_for             = datas.get("avg_offside_for", 0),
                    avg_offside_against         = datas.get("avg_offside_against", 0),
                    avg_cards_for               = datas.get("avg_cards_for", 0),
                    avg_cards_against           = datas.get("avg_cards_against", 0),
                )
            instance.is_stated = True
            
            
            before_stats_match(instance)
            instance.is_compared = True
            
            get_home_facts.function(instance)
            get_away_facts.function(instance)
            instance.is_facted = True
            
            instance.save()
            
    except Exception as e:
        print("----------error save match----------", e)
            
