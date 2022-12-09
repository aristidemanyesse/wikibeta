from django.db import models
from django.db import models
from django.db.models import Avg, Sum, Q
from core.models import BaseModel, Etat
from django.core.validators import MinValueValidator
from fractions import Fraction
from core.functions import *
# Create your models here.

from features.models import Match



class ModePrediction(BaseModel):
    name          = models.CharField(max_length = 255, null = True, blank=True)
    description   = models.CharField(max_length = 255, null = True, blank=True)

    @classmethod
    def get(cls, mode):
        return cls.objects.get(name = mode)


    

class TypePrediction(BaseModel):
    name          = models.CharField(max_length = 255, null = True, blank=True)
    description   = models.CharField(max_length = 255, null = True, blank=True)

    @classmethod
    def get(cls, type):
        return cls.objects.get(name = type)
    
    

class Prediction(BaseModel):
    mode          = models.ForeignKey(ModePrediction, null = True, blank=True, on_delete = models.CASCADE, related_name="prediction_mode")
    type          = models.ForeignKey(TypePrediction, on_delete = models.CASCADE, related_name="prediction_type")
    match         = models.ForeignKey(Match, on_delete = models.CASCADE, related_name="prediction_match")
    pct           = models.FloatField(default = 0.0, null = True, blank=True)
    is_checked    = models.BooleanField(null = True, blank=True)

    def __str__(self):
        return str(self.type)+": "+self.predicition
    