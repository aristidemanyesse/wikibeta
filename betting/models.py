from django.db import models
from django.db.models import Avg, Sum
from core.models import BaseModel, Etat
from django.core.validators import MinValueValidator

from features.models import Match


class Bookmaker(BaseModel):
    name    = models.CharField(max_length = 255, null = True, blank=True)
    code    = models.CharField(max_length = 255, null = True, blank=True)


class OddsMatch(BaseModel):
    match   = models.ForeignKey(Match, on_delete = models.CASCADE, related_name="match_odds")
    booker    = models.ForeignKey(Bookmaker, on_delete = models.CASCADE, related_name="booker_match")
    home    = models.IntegerField(default = 1, null = True, blank=True)
    draw    = models.IntegerField(default = 1, null = True, blank=True)
    away    = models.IntegerField(default = 1, null = True, blank=True)
