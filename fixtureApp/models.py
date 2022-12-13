from django.db import models
from django.db.models import Avg, Sum, Q
from annoying.decorators import signals
from coreApp.models import BaseModel
from coreApp.functions import *
from teamApp.models import *
from statsApp.models import *
from bettingApp.models import *


class Match(BaseModel):
    date              = models.DateField( null = True, blank=True)
    hour              = models.TimeField( null = True, blank=True)
    home              = models.ForeignKey("teamApp.EditionTeam", on_delete = models.CASCADE, related_name="home_match")
    away              = models.ForeignKey("teamApp.EditionTeam", on_delete = models.CASCADE, related_name="away_match")
    edition           = models.ForeignKey("competitionApp.EditionCompetition", on_delete = models.CASCADE, related_name="edition_du_match")
    is_finished        = models.BooleanField(default = False, null = True, blank=True)

    class Meta:
        ordering = ['date']
    
    
    def __str__(self):
        return str(self.home) +" -VS- "+ str(self.away)


    def get_result(self):
        return self.result_match.filter().first()
       
    
    def confrontations_directes(self, number = 50):
        matchs = Match.objects.filter(Q(home__team = self.home.team, away__team = self.away.team) | Q(home__team = self.away.team,  away__team = self.home.team)).filter(date__lt = self.date).exclude(id = self.id).order_by("-date")        
        return matchs[:number]
    
    
    def similaires_ppg(self, number = 50):
        matchs = []
        ppg_home = self.before_stat_match.filter(team = self.home).first().ppg
        ppg_away = self.before_stat_match.filter(team = self.away).first().ppg
        
        befores = BeforeMatchStat.objects.filter(ppg__range = intervale(ppg_home), match__edition__competition = self.edition.competition, match__date__lt = self.date).exclude(id = self.id).order_by("-match__date")
        for bef in befores:
            if bef.team == bef.match.home:
                befs = BeforeMatchStat.objects.filter(ppg__range = intervale(ppg_away), match = bef.match).exclude(id = bef.id)
                if len(befs) == 1:
                    matchs.append(bef.match)
                
        return matchs[:number]


    def similaires_betting(self, number = 50):
        matchs = []
        actual = self.match_odds.filter(booker__code = "B365").first()
        if actual is not None:
            odds = OddsMatch.objects.filter(home__range = intervale(actual.home), match__edition__competition = self.edition.competition, match__date__lt = self.date).exclude(id = self.id).order_by("-match__date")
            for odd in odds:
                if intervale(odd.home) == intervale(actual.home):
                    befs = OddsMatch.objects.filter(away__range = intervale(actual.away), match = odd.match).exclude(id = odd.id)
                    if len(befs) == 1:
                        matchs.append(odd.match)
                    
        return matchs[:number]
    
    

    def get_odds(self, code = "B365"):
        return self.match_odds.filter(booker__code = code).first()
    



    
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
    if created:
        #creation du before stat pour chaque equipe
        for team in [instance.home, instance.away]:
            points, ppg, scored, avg_goals_scored, conceded, avg_goals_conceded = team.last_stats(instance, edition = True)
            
            BeforeMatchStat.objects.create(
                match = instance,
                team = instance.home if (instance.home == team) else instance.away,
                ppg = ppg,
                goals_scored = scored,
                avg_goals_scored = avg_goals_scored,
                goals_conceded = conceded,
                avg_goals_conceded = avg_goals_conceded
            )