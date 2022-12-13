from django.db import models
from django.db.models import Avg, Sum
from coreApp.models import BaseModel


class Bookmaker(BaseModel):
    name    = models.CharField(max_length = 255, null = True, blank=True)
    code    = models.CharField(max_length = 255, null = True, blank=True)


class OddsMatch(BaseModel):
    match   = models.ForeignKey("fixtureApp.Match", on_delete = models.CASCADE, related_name="match_odds")
    booker    = models.ForeignKey(Bookmaker, on_delete = models.CASCADE, related_name="booker_match")
    home    = models.FloatField(default = 1.0, null = True, blank=True)
    draw    = models.FloatField(default = 1.0, null = True, blank=True)
    away    = models.FloatField(default = 1.0, null = True, blank=True)

    def __str__(self):
        return str(self.match)