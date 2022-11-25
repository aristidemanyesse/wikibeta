from django.db import models
from django.db.models import Avg, Sum
from core.models import BaseModel, Etat
from django.core.validators import MinValueValidator


class Pays(BaseModel):
    name    = models.CharField(max_length = 255, null = True, blank=True)
    code    = models.CharField(max_length = 255, null = True, blank=True)


class Competition(BaseModel):
    name    = models.CharField(max_length = 255, null = False, blank=False)
    code    = models.CharField(max_length = 255, null = True, blank=True)
    pays    = models.ForeignKey(Pays, on_delete = models.CASCADE, related_name="pays_de_competition")


class Edition(BaseModel):
    name    = models.CharField(max_length = 255, null = False, blank=False)
    start_date    = models.DateField(default = "", null = True, blank=True)
    finish_date    = models.DateField(default = "", null = True, blank=True)
    competition    = models.ForeignKey(Competition, on_delete = models.CASCADE, related_name="competition_edition")


class Team(BaseModel):
    name    = models.CharField(max_length = 255, null = False, blank=False)
    code    = models.CharField(max_length = 255, null = True, blank=True)
    pays    = models.ForeignKey(Pays, on_delete = models.CASCADE, related_name="pays_du_team")
    logo       = models.CharField(max_length = 255, null = False, blank=False)


class EditionTeam(BaseModel):
    edition    = models.ForeignKey(Edition, on_delete = models.CASCADE, related_name="edition_team")
    team    = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="team_edition")
    
    
class Match(BaseModel):
    home            = models.ForeignKey(EditionTeam, on_delete = models.CASCADE, related_name="home_team")
    away            = models.ForeignKey(EditionTeam, on_delete = models.CASCADE, related_name="away_team")
    home_ft_score   = models.IntegerField(default = 0, null = True, blank=True)
    away_ft_score   = models.IntegerField(default = 0, null = True, blank=True)
    result_ft       = models.CharField(max_length = 255, null = False, blank=False)
    home_half_score = models.IntegerField(default = 0, null = True, blank=True)
    away_half_score = models.IntegerField(default = 0, null = True, blank=True)
    result_half     = models.CharField(max_length = 255, null = False, blank=False)
    edition         = models.ForeignKey(Edition, on_delete = models.CASCADE, related_name="edition_du_match")


class Goal(BaseModel):
    match             = models.ForeignKey(Match, on_delete = models.CASCADE, related_name="goal_du_match")
    team              = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="team_du_goal")
    minute            = models.CharField(max_length = 255, null = False, blank=False)
    is_penalty        = models.BooleanField(max_length = 255, null = False, blank=False)
    home_half_score   = models.IntegerField(default = 0, null = True, blank=True)
    away_half_score   = models.IntegerField(default = 0, null = True, blank=True)

        
    def acompte_actuel(self):

        return True

