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
        return cls.objects.get(code = type)
    
    

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
            
            if self.type.code == "p1_5":
                self.is_checked = (result.home_score + result.away_score) > 1.5
            if self.type.code == "p2_5":
                self.is_checked = (result.home_score + result.away_score) > 2.5
            if self.type.code == "p3_5":
                self.is_checked = (result.home_score + result.away_score) > 3.5
            if self.type.code == "m1_5":
                self.is_checked = (result.home_score + result.away_score) < 1.5
            if self.type.code == "m2_5":
                self.is_checked = (result.home_score + result.away_score) < 2.5
            if self.type.code == "m3_5":
                self.is_checked = (result.home_score + result.away_score) < 3.5
            if self.type.code == "1X":
                self.is_checked = result.home_score >= result.away_score
            if self.type.code == "12":
                self.is_checked = result.home_score != result.away_score
            if self.type.code == "X2":
                self.is_checked = result.home_score <= result.away_score
            if self.type.code == "HG":
                self.is_checked = result.home_score > 0
            if self.type.code == "AG":
                self.is_checked =result.away_score > 0
            if self.type.code == "btts":
                self.is_checked = result.home_score > 0 and result.away_score > 0
            if self.type.code == "no_btts":
                self.is_checked = (result.home_score > 0 and result.away_score == 0) or (result.home_score == 0 and result.away_score > 0)
            if self.type.code == "corner_p6_5":
                self.is_checked = (extra.home_corners or 0 )+ (extra.away_corners or 0) > 8.5
            if self.type.code == "corner_m12_5":
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
        try :
            if self.match.is_finished:
                result = self.match.get_result()
                extra = self.match.get_extra_info_match()
                
                                
                if self.type.code == "p0_5_MT":
                    if result.home_half_score is not None:
                        self.is_checked = (result.home_half_score + result.away_half_score) > 0.5
                        
                elif self.type.code == "p1_5":
                    self.is_checked = (result.home_score + result.away_score) > 1.5
                    
                elif self.type.code == "p2_5":
                    self.is_checked = (result.home_score + result.away_score) > 2.5
                    
                elif self.type.code == "p3_5":
                    self.is_checked = (result.home_score + result.away_score) > 3.5
                    
                elif self.type.code == "m1_5_MT":
                    if result.home_half_score is not None:
                        self.is_checked = (result.home_half_score + result.away_half_score) < 1.5
                        
                elif self.type.code == "m3_5":
                    self.is_checked = (result.home_score + result.away_score) < 3.5
                    
                elif self.type.code == "1":
                    self.is_checked = result.home_score > result.away_score

                elif self.type.code == "1X":
                    self.is_checked = result.home_score >= result.away_score

                elif self.type.code == "12":
                    self.is_checked = result.home_score != result.away_score

                elif self.type.code == "X":
                    self.is_checked = result.home_score == result.away_score

                elif self.type.code == "2":
                    self.is_checked = result.home_score < result.away_score

                elif self.type.code == "X2":
                    self.is_checked = result.home_score <= result.away_score

                elif self.type.code == "HG":
                    self.is_checked = result.home_score > 0
                    
                elif self.type.code == "AG":
                    self.is_checked =result.away_score > 0

                elif self.type.code == "HG|2":
                    self.is_checked = not result.home_score > 1.5

                elif self.type.code == "AG|2":
                    self.is_checked = not result.away_score > 1.5

                elif self.type.code == "btts":
                    self.is_checked = result.home_score > 0 and result.away_score > 0

                elif self.type.code == "no_btts":
                    self.is_checked = (result.home_score > 0 and result.away_score == 0) or (result.home_score == 0 and result.away_score > 0)

                

                elif self.type.code == "corner_p6_5":
                    self.is_checked = extra.home_corners + extra.away_corners > 6.5

                # elif self.type.code == "corner_m12_5":
                #     self.is_checked = extra.home_corners + extra.away_corners < 12.5
                elif self.type.code == "corner_m12_5":
                    self.is_checked = extra.home_corners < 8.5 and extra.away_corners < 8.5

                elif self.type.code == "1C":
                    self.is_checked = extra.home_corners >= extra.away_corners

                elif self.type.code == "2C":
                    self.is_checked = extra.home_corners <= extra.away_corners


                elif self.type.code == "foul_p20_5":
                    self.is_checked = extra.home_fouls + extra.away_fouls > 20.5

                elif self.type.code == "foul_m30_5":
                    self.is_checked = extra.home_fouls + extra.away_fouls < 30.5


                elif self.type.code == "shoot_target_p6_5":
                    self.is_checked = extra.home_shots_on_target + extra.away_shots_on_target > 5.5

                elif self.type.code == "shoot_target_m11_5":
                    self.is_checked = extra.home_shots_on_target + extra.away_shots_on_target < 11.5


                elif self.type.code == "shoot_p20_5":
                    self.is_checked = extra.home_shots + extra.away_shots > 20.5

                elif self.type.code == "shoot_m30_5":
                    self.is_checked = extra.home_shots + extra.away_shots < 30.5


                elif self.type.code == "card_p2_5":
                    self.is_checked = extra.home_yellow_cards + extra.away_yellow_cards > 2.5

                elif self.type.code == "card_m5_5":
                    self.is_checked = extra.home_yellow_cards + extra.away_yellow_cards < 5.5

                self.save()
                
        except Exception as e:
            print("Error validating predictions test: " + str(e))
            
            


class PredictionScore(BaseModel):
    match         = models.ForeignKey("fixtureApp.Match", on_delete = models.CASCADE, related_name="predictionscore_match")
    home_score    = models.IntegerField(default = 0.00, null = True, blank=True)
    away_score    = models.IntegerField(default = 0, null = True, blank=True)
    pct           = models.FloatField(default = 0, null = True, blank=True)
    is_checked    = models.BooleanField(null = True, blank=True)

    def __str__(self):
        return f"{self.home_score}-{self.away_score}"
        # return f"{self.home_score}-{self.away_score} = {round(self.pct, 2)}"
        # return str(self.match)+": "+str(self.pct)
    
    class Meta:
        ordering = ['match', '-pct', 'is_checked']
        
    
    
    def validity(self):
        if self.match.is_finished:
            result = self.match.get_result()
            self.is_checked = (self.home_score == result.home_score and self.away_score == result.away_score)
            self.save()
            
    
    def total(self):
        return self.home_score + self.away_score