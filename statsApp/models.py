from django.db import models
from django.db.models import Avg, Sum, Q
from coreApp.models import BaseModel
from fixtureApp.models import *
from coreApp.functions import *



class BeforeMatchStat(BaseModel):   
    match               = models.ForeignKey("fixtureApp.Match", on_delete = models.CASCADE, related_name="before_stat_match")
    team                = models.ForeignKey("teamApp.EditionTeam", null = True, blank=True, on_delete = models.CASCADE, related_name="team_stat_match")
    ppg                 = models.FloatField(null = True, blank=True)
    goals_scored        = models.FloatField(null = True, blank=True)
    avg_goals_scored    = models.FloatField(null = True, blank=True)
    goals_conceded      = models.FloatField(null = True, blank=True)
    avg_goals_conceded  = models.FloatField(null = True, blank=True)

    def __str__(self):
        return str(self.match)



class ResultMatch(BaseModel):
    match              = models.ForeignKey("fixtureApp.Match", on_delete = models.CASCADE, related_name="result_match")
    home_score        = models.IntegerField(default = 0, null = True, blank=True)
    away_score        = models.IntegerField(default = 0, null = True, blank=True)
    result            = models.CharField(max_length = 255, null = True, blank=True)
    home_half_score   = models.IntegerField(default = 0, null = True, blank=True)
    away_half_score   = models.IntegerField(default = 0, null = True, blank=True)
    result_half       = models.CharField(max_length = 255, null = True, blank=True)

    def __str__(self):
        return str(self.match)+" (resultast)"
    
class ExtraInfosMatch(BaseModel):
    match                   = models.ForeignKey("fixtureApp.Match", on_delete = models.CASCADE, related_name="extra_match")
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
    