from django.db import models
from django.db.models import Avg, Sum, Q
from coreApp.models import BaseModel
from coreApp.functions import *
from competitionApp.models import *

    
class Team(BaseModel):
    name    = models.CharField(max_length = 255, null = True, blank=True)
    code    = models.CharField(max_length = 255, null = True, blank=True)
    pays    = models.ForeignKey("competitionApp.Pays", on_delete = models.CASCADE, related_name="pays_du_team")
    logo    = models.ImageField(max_length = 255, upload_to = "static/images/team/", default="", null = True, blank=True)
    
    def __str__(self):
        return self.name




class EditionTeam(BaseModel):
    NB = 7
    edition   = models.ForeignKey("competitionApp.EditionCompetition", on_delete = models.CASCADE, related_name="edition_team")
    team      = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="team_edition")

    class Meta:
        ordering = ['-edition']
        
    def __str__(self):
        return str(self.team)
    

    def get_last_away_matchs(self, match, number : None):
        matchs = self.away_match.filter(date__lt = match.date).order_by("-date")
        return matchs[:EditionTeam.NB if number is None else number]
    
    
    def get_recents_matchs(self, match, number : None):
        matchs = self.edition.edition_du_match.filter(date__lt = match.date).filter(Q(home = self) | Q(away = self)).order_by("-date")
        return matchs[:EditionTeam.NB if number is None else number]
    
    
    def get_last_form(self, match):
        matchs = self.get_recents_matchs(match)
        return [x.form(self) for x in matchs[:EditionTeam.NB]]
    
    
    def plus_but(self, nb):
        matchs = Match.objects.filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            if match.home_score + match.away_score > nb:
                total += 1
        return total


    def moins_but(self, nb):
        matchs = Match.objects.filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            if match.home_score + match.away_score < nb:
                total += 1
        return total
    
    
    def ht_plus_but(self, nb):
        matchs = Match.objects.filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            if match.home_half_score is not None :
                if match.home_half_score + match.away_half_score > nb:
                    total += 1
        return total


    def ht_moins_but(self, nb):
        matchs = Match.objects.filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            if match.home_half_score is not None :
                if match.home_half_score + match.away_half_score < nb:
                    total += 1
        return total
    
    
    
    
    