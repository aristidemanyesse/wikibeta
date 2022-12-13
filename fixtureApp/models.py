from django.db import models
from django.db.models import Avg, Sum, Q
from coreApp.models import BaseModel
from coreApp.functions import *
from teamApp.models import *
from statsApp.models import *


class Match(BaseModel):
    date              = models.DateField( null = True, blank=True)
    hour              = models.TimeField( null = True, blank=True)
    home              = models.ForeignKey("teamApp.EditionTeam", on_delete = models.CASCADE, related_name="home_match")
    away              = models.ForeignKey("teamApp.EditionTeam", on_delete = models.CASCADE, related_name="away_match")
    edition           = models.ForeignKey("competitionApp.EditionCompetition", on_delete = models.CASCADE, related_name="edition_du_match")
    is_finished        = models.BooleanField(default = False, null = True, blank=True)

    class Meta:
        ordering = ['date']
    
    
    def finished(self, row, header):
        return str(self.home) +" -VS- "+ str(self.away)

        

    def __str__(self):
        return str(self.home) +" -VS- "+ str(self.away)


    def score(self):
        return str(self.home_score) +" - "+ str(self.away_score)
       
    
    def confrontations_directes(self):
        matchs = Match.objects.filter(Q(home__team = self.home.team, away__team = self.away.team) | Q(home__team = self.away.team,  away__team = self.home.team)).filter(date__lt = self.date).exclude(id = self.id).order_by("-date")        
        return matchs
    
    
    def similaires_ppg(self):
        matchs = []
        ppg_home = self.before_stat_match.filter(team = self.home).first().ppg
        ppg_away = self.before_stat_match.filter(team = self.away).first().ppg
        
        befores = BeforeMatchStat.objects.filter(ppg__range = intervale(ppg_home), match__edition__competition = self.edition.competition, match__date__lt = self.date).exclude(id = self.id).order_by("-match__date")
        for bef in befores:
            if bef.team == bef.match.home:
                befs = BeforeMatchStat.objects.filter(ppg__range = intervale(ppg_away), match = bef.match).exclude(id = bef.id)
                if len(befs) == 1:
                    matchs.append(bef.match)
                
        return matchs[:50]


    def similaires_betting(self):
        matchs = []
        actual = self.match_odds.filter(booker__code = "B365").first()
        if actual is not None:
            odds = OddsMatch.objects.filter(home__range = intervale(actual.home), match__edition__competition = self.edition.competition, match__date__lt = self.date).exclude(id = self.id).order_by("-match__date")
            for odd in odds:
                if intervale(odd.home) == intervale(actual.home):
                    befs = OddsMatch.objects.filter(away__range = intervale(actual.away), match = odd.match).exclude(id = odd.id)
                    if len(befs) == 1:
                        matchs.append(odd.match)
                    
        return matchs[:50]
    
    
    
    def form(self, team : EditionTeam):
        if team in [self.home, self.away] :
            if self.result == "D":
                return "N"
            elif self.result == "H":
                return "V" if (self.home == team) else "D"
            elif self.result == "A":
                return "V" if (self.away == team) else "D"
    
    
    def points_for_this_macth(self, team : EditionTeam):
        if team == self.home or team == self.away:
            if self.result == "D":
                return 1
            elif self.result == "H":
                return 3 if (self.home == team) else 0
            elif self.result == "A":
                return 3 if (self.away == team) else 0
        return 0
        
        
    def goals_scored(self, team : EditionTeam):
        if team == self.home or team == self.away:
            return self.home_score if self.home == team else self.away_score
        return 0
    

    def goals_conceded(self, team : EditionTeam):
        if team == self.home or team == self.away:
            return self.away_score if self.home == team else self.home_score
        return 0
    
    
    def get_home_recents_matchs(self, number = None, edition = False):
        if edition:
            matchs = Match.objects.filter(date__lt = self.date).filter(Q(home = self.home) | Q(away = self.home)).exclude(id  = self.id).order_by("-date")
        else:
            matchs = Match.objects.filter(date__lt = self.date).filter(Q(home__team = self.home.team) | Q(away__team = self.home.team)).exclude(id  = self.id).order_by("-date")
        return matchs[:EditionTeam.NB if number is None else number]


    def get_away_recents_matchs(self, number = None, edition = False):
        if edition:
            matchs = Match.objects.filter(date__lt = self.date).filter(Q(home = self.away) | Q(away = self.away)).exclude(id  = self.id).order_by("-date")
        else:
            matchs = Match.objects.filter(date__lt = self.date).filter(Q(home__team = self.away.team) | Q(away__team = self.away.team)).exclude(id  = self.id).order_by("-date")
        return matchs[:EditionTeam.NB if number is None else number]


    def get_home_last_form(self):
        return [x.form(self.home) for x in self.get_home_recents_matchs(edition=True)]


    def get_away_last_form(self):
        return [x.form(self.away) for x in self.get_away_recents_matchs(edition=True)]
      
      
        
    def get_home_before_stats(self):
        return self.before_stat_match.filter(team = self.home).first()

    def get_away_before_stats(self):
        return self.before_stat_match.filter(team = self.away).first()  

    def get_home_extra_info(self):
        return self.extra_match.filter(team = self.home).first()

    def get_away_extra_info(self):
        return self.extra_match.filter(team = self.away).first()

    def get_bet365(self):
        return self.match_odds.filter(booker__code = "B365").first()
    

    
class Goal(BaseModel):
    match             = models.ForeignKey("fixtureApp.Match", on_delete = models.CASCADE, related_name="goal_du_match")
    team              = models.ForeignKey("teamApp.Team", on_delete = models.CASCADE, related_name="team_du_goal")
    minute            = models.CharField(max_length = 255, null = True, blank=True)
    is_penalty        = models.BooleanField(default = False, null = True, blank=True)
    home_half_score   = models.IntegerField(default = 0, null = True, blank=True)
    away_half_score   = models.IntegerField(default = 0, null = True, blank=True)

    def __str__(self):
        return str(self.team) +" goal in "+ str(self.match)


