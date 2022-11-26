from django.db import models
from django.db.models import Avg, Sum
from core.models import BaseModel, Etat
from django.core.validators import MinValueValidator


class Pays(BaseModel):
    name    = models.CharField(max_length = 255, null = True, blank=True)
    code    = models.CharField(max_length = 255, null = True, blank=True)

    def __str__(self):
        return self.name


class Competition(BaseModel):
    name    = models.CharField(max_length = 255, null = True, blank=True)
    code    = models.CharField(max_length = 255, null = True, blank=True)
    pays    = models.ForeignKey(Pays, on_delete = models.CASCADE, related_name="pays_de_competition")

    def __str__(self):
        return self.name


class Edition(BaseModel):
    name          = models.CharField(max_length = 255, null = True, blank=True)
    start_date    = models.DateField(null = True, blank=True)
    finish_date   = models.DateField(null = True, blank=True)

    def __str__(self):
        return self.name

class EditionCompetition(BaseModel):
    edition       = models.ForeignKey(Edition, on_delete = models.CASCADE, related_name="edition_team")
    competition   = models.ForeignKey(Competition, on_delete = models.CASCADE, related_name="competition_edition")

    def __str__(self):
        return str(self.competition) +" - "+ str(self.edition)

class Team(BaseModel):
    name    = models.CharField(max_length = 255, null = True, blank=True)
    code    = models.CharField(max_length = 255, null = True, blank=True)
    pays    = models.ForeignKey(Pays, on_delete = models.CASCADE, related_name="pays_du_team")
    logo    = models.CharField(max_length = 255, null = True, blank=True)
    
    def __str__(self):
        return self.name


class EditionTeam(BaseModel):
    edition   = models.ForeignKey(EditionCompetition, on_delete = models.CASCADE, related_name="edition_team")
    team      = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="team_edition")

    def __str__(self):
        return str(self.team)
    
class Match(BaseModel):
    date              = models.DateField( null = True, blank=True)
    home              = models.ForeignKey(EditionTeam, on_delete = models.CASCADE, related_name="home_team")
    away              = models.ForeignKey(EditionTeam, on_delete = models.CASCADE, related_name="away_team")
    home_score        = models.IntegerField(default = 0, null = True, blank=True)
    away_score        = models.IntegerField(default = 0, null = True, blank=True)
    result            = models.CharField(max_length = 255, null = True, blank=True)
    home_half_score   = models.IntegerField(default = 0, null = True, blank=True)
    away_half_score   = models.IntegerField(default = 0, null = True, blank=True)
    result_half       = models.CharField(max_length = 255, null = True, blank=True)
    edition           = models.ForeignKey(EditionCompetition, on_delete = models.CASCADE, related_name="edition_du_match")

    def __str__(self):
        return str(self.home) +" -VS- "+ str(self.away)


class ExtraInfosMatch(BaseModel):
    match                   = models.ForeignKey(Match, on_delete = models.CASCADE, related_name="extra_match")
    home_shots              = models.IntegerField(default = 0, null = True, blank=True)
    away_shots              = models.IntegerField(default = 0, null = True, blank=True)
    home_shots_on_target    = models.IntegerField(default = 0, null = True, blank=True)
    away_shots_on_target    = models.IntegerField(default = 0, null = True, blank=True)
    home_corners            = models.IntegerField(default = 0, null = True, blank=True)
    away_corners            = models.IntegerField(default = 0, null = True, blank=True)
    home_fouls              = models.IntegerField(default = 0, null = True, blank=True)
    away_fouls              = models.IntegerField(default = 0, null = True, blank=True)
    home_offsides           = models.IntegerField(default = 0, null = True, blank=True)
    away_offsides           = models.IntegerField(default = 0, null = True, blank=True)
    home_yellow_cards       = models.IntegerField(default = 0, null = True, blank=True)
    away_yellow_cards       = models.IntegerField(default = 0, null = True, blank=True)
    home_red_cards          = models.IntegerField(default = 0, null = True, blank=True)
    away_red_cards          = models.IntegerField(default = 0, null = True, blank=True)
    
    def __str__(self):
        return str(self.match) +" (extra infos)"
    
    
class Goal(BaseModel):
    match             = models.ForeignKey(Match, on_delete = models.CASCADE, related_name="goal_du_match")
    team              = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="team_du_goal")
    minute            = models.CharField(max_length = 255, null = True, blank=True)
    is_penalty        = models.BooleanField(max_length = 255, null = True, blank=True)
    home_half_score   = models.IntegerField(default = 0, null = True, blank=True)
    away_half_score   = models.IntegerField(default = 0, null = True, blank=True)

    def __str__(self):
        return str(self.team) +" goal in "+ str(self.match)


