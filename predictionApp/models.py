from django.db import models
from django.db import models
from django.db.models import Avg, Sum, Q
from coreApp.models import BaseModel
from coreApp.functions import *
# Create your models here.


class ModePrediction(BaseModel):
    name          = models.CharField(max_length = 255, null = True, blank=True)
    description   = models.CharField(max_length = 255, null = True, blank=True)

    @classmethod
    def get(cls, mode):
        return cls.objects.get(name = mode)


    def ratio_by_type(self, type):
        total = Prediction.objects.filter(type = type, mode = self).exclude(is_checked = None)
        return round((total.filter(is_checked = True).count() / total.count()) *100, 2) if total.count() > 0 else 0
    

class TypePrediction(BaseModel):
    name          = models.CharField(max_length = 255, null = True, blank=True)
    code          = models.CharField(max_length = 255, null = True, blank=True)
    description   = models.CharField(max_length = 255, null = True, blank=True)

    @classmethod
    def get(cls, type):
        return cls.objects.get(name = type)
    
    

class Prediction(BaseModel):
    mode          = models.ForeignKey(ModePrediction, null = True, blank=True, on_delete = models.CASCADE, related_name="prediction_mode")
    type          = models.ForeignKey(TypePrediction, on_delete = models.CASCADE, related_name="prediction_type")
    match         = models.ForeignKey("fixtureApp.Match", on_delete = models.CASCADE, related_name="prediction_match")
    pct           = models.FloatField(default = 0.00, null = True, blank=True)
    is_checked    = models.BooleanField(null = True, blank=True)

    def __str__(self):
        return str(self.type)+": "+str(self.pct)


    def validity(self):
        if self.match.is_finished:
            result = self.match.get_result()
            extra = self.match.get_extra_info_match()
            
            if self.type == TypePrediction.get("p1_5"):
                self.is_checked = (result.home_score + result.away_score) > 1.5
            if self.type == TypePrediction.get("p2_5"):
                self.is_checked = (result.home_score + result.away_score) > 2.5
            if self.type == TypePrediction.get("p3_5"):
                self.is_checked = (result.home_score + result.away_score) > 3.5
            if self.type == TypePrediction.get("m1_5"):
                self.is_checked = (result.home_score + result.away_score) < 1.5
            if self.type == TypePrediction.get("m2_5"):
                self.is_checked = (result.home_score + result.away_score) < 2.5
            if self.type == TypePrediction.get("m3_5"):
                self.is_checked = (result.home_score + result.away_score) < 3.5
            if self.type == TypePrediction.get("VN_Home"):
                self.is_checked = result.home_score >= result.away_score
            if self.type == TypePrediction.get("12"):
                self.is_checked = result.home_score != result.away_score
            if self.type == TypePrediction.get("VN_Away"):
                self.is_checked = result.home_score <= result.away_score
            if self.type == TypePrediction.get("But_Home"):
                self.is_checked = result.home_score > 0
            if self.type == TypePrediction.get("But_Away"):
                self.is_checked =result.away_score > 0
            if self.type == TypePrediction.get("btts"):
                self.is_checked = result.home_score > 0 and result.away_score > 0
            if self.type == TypePrediction.get("no_btts"):
                self.is_checked = (result.home_score > 0 and result.away_score == 0) or (result.home_score == 0 and result.away_score > 0)
            if self.type == TypePrediction.get("corner_p8_5"):
                self.is_checked = (extra.home_corners or 0 )+ (extra.away_corners or 0) > 8.5
            if self.type == TypePrediction.get("corner_m12_5"):
                self.is_checked = (extra.home_corners or 0 )+ (extra.away_corners or 0) < 12.5
            self.save()
            
            
            
            

class PredictionTest(BaseModel):
    mode          = models.ForeignKey(ModePrediction, null = True, blank=True, on_delete = models.CASCADE, related_name="predictiontest_mode")
    type          = models.ForeignKey(TypePrediction, on_delete = models.CASCADE, related_name="predictiontest_type")
    match         = models.ForeignKey("fixtureApp.Match", on_delete = models.CASCADE, related_name="predictiontest_match")
    pct           = models.FloatField(default = 0.00, null = True, blank=True)
    is_checked    = models.BooleanField(null = True, blank=True)

    def __str__(self):
        return str(self.type)+": "+str(self.pct)


    def validity(self):
        if self.match.is_finished:
            result = self.match.get_result()
            extra = self.match.get_extra_info_match()
            
            if self.type == TypePrediction.get("p1_5"):
                self.is_checked = (result.home_score + result.away_score) > 1.5
            if self.type == TypePrediction.get("p2_5"):
                self.is_checked = (result.home_score + result.away_score) > 2.5
            if self.type == TypePrediction.get("p3_5"):
                self.is_checked = (result.home_score + result.away_score) > 3.5
            if self.type == TypePrediction.get("m1_5"):
                self.is_checked = (result.home_score + result.away_score) < 1.5
            if self.type == TypePrediction.get("m2_5"):
                self.is_checked = (result.home_score + result.away_score) < 2.5
            if self.type == TypePrediction.get("m3_5"):
                self.is_checked = (result.home_score + result.away_score) < 3.5
            if self.type == TypePrediction.get("VN_Home"):
                self.is_checked = result.home_score >= result.away_score
            if self.type == TypePrediction.get("12"):
                self.is_checked = result.home_score != result.away_score
            if self.type == TypePrediction.get("VN_Away"):
                self.is_checked = result.home_score <= result.away_score
            if self.type == TypePrediction.get("But_Home"):
                self.is_checked = result.home_score > 0
            if self.type == TypePrediction.get("But_Away"):
                self.is_checked =result.away_score > 0
            if self.type == TypePrediction.get("btts"):
                self.is_checked = result.home_score > 0 and result.away_score > 0
            if self.type == TypePrediction.get("no_btts"):
                self.is_checked = (result.home_score > 0 and result.away_score == 0) or (result.home_score == 0 and result.away_score > 0)
            if self.type == TypePrediction.get("corner_p8_5"):
                self.is_checked = (extra.home_corners or 0 )+ (extra.away_corners or 0) > 8.5
            if self.type == TypePrediction.get("corner_m12_5"):
                self.is_checked = (extra.home_corners or 0 )+ (extra.away_corners or 0) < 12.5
            self.save()