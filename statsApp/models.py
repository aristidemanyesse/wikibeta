from django.db import models
from django.db.models import Avg, Sum, Q
from coreApp.models import BaseModel
from annoying.decorators import signals
import json


class TypeFact(BaseModel):   
    name    = models.CharField(max_length = 255, null = True, blank=True)
    description    = models.CharField(max_length = 255, null = True, blank=True)

class Fact(BaseModel):       
    type        = models.ForeignKey(TypeFact , null = True, blank=True, on_delete = models.CASCADE, related_name="type_facts")
    match       = models.ForeignKey("fixtureApp.Match", on_delete = models.CASCADE, related_name="match_facts")
    team        = models.ForeignKey("teamApp.EditionTeam", null = True, blank=True, on_delete = models.CASCADE, related_name="team_facts")
    full_time   = models.BooleanField(null = True, blank=True)
    all_matches = models.BooleanField(null = True, blank=True)
    total       = models.IntegerField(null = True, blank=True)
    success     = models.IntegerField(null = True, blank=True)
    pct         = models.FloatField(null = True, blank=True)

    def __str__(self):
        return str(self.match)


    def sentence(self):
        prefixe = suffixe = sentence = ""
        if not self.all_matches:
            suffixe = "à domicile !" if self.match.home == self.team else "à l'extérieur !"
            
        if (self.pct == 0 or self.pct == 1) and (self.type.name not in ["TGS", "TGC"]):
            if self.type.name == "Win":
                prefixe = "Que des " if self.pct == 1 else "Aucun(e)"
                sentence = "victoires lors des {} derniers matchs".format(self.total)
            if self.type.name == "Draw":
                prefixe = "Que des " if self.pct == 1 else "Aucun(e)"
                sentence = "nuls lors des {} derniers matchs".format(self.total)
            if self.type.name == "Lose":
                prefixe = "Que des " if self.pct == 1 else "Aucun(e)"
                sentence = "defaites lors des {} derniers matchs".format(self.total)
            

            if self.type.name == "btts":
                sentence = "Les deux équipes ont marqué lors des {} derniers matchs ".format(self.total)
                if self.pct == 0:
                    sentence = "les deux équipes n'ont pas marqué lors des {} derniers matchs ".format(self.total)
                    
            if self.type.name == "CS":
                sentence = "Que des clean sheets lors des {} derniers matchs".format(self.total)
                if self.pct == 0:
                    sentence = "Aucun clean sheet lors des {} derniers matchs".format(self.total)
                    
            if self.type.name == "GS":
                sentence = "Au moins 1 but marqué lors des {} derniers matchs".format(self.total)
                if self.pct == 0:
                    sentence = "Aucun but marqué lors des {} derniers matchs".format(self.total)
                    
            if self.type.name == "GC":
                sentence = "Au moins 1 but concédé lors des {} derniers matchs".format(self.total)
                if self.pct == 0:
                    sentence = "Aucun but concédé lors des {} derniers matchs".format(self.total)
                    
            if self.type.name == "p1_5":
                sentence = "Total d'au moins 2 buts lors des {} derniers matchs".format(self.total)
                if self.pct == 0:
                    sentence = "Aucun match avec au moins 2 buts lors des {} derniers matchs".format(self.total)         
                       
            if self.type.name == "m3_5":
                sentence = "Pas plus de 3 buts lors des {} derniers matchs".format(self.total)
                if self.pct == 0:
                    sentence = "Plus de 3 buts lors des {} derniers matchs".format(self.total)
                    
        else :  
            prefixe = ""
            if self.pct <= 0.2:
                prefixe = "Seulement "
                
            if self.type.name == "Win":
                sentence = "{} victoires lors des {} derniers matchs".format(self.success, self.total)
            if self.type.name == "Draw":
                sentence = "{} nuls lors des {} derniers matchs".format(self.success, self.total)
            if self.type.name == "Lose":
                sentence = "{} defaites lors des {} derniers matchs".format(self.success, self.total)
            if self.type.name == "btts":
                sentence = "{} matchs sur les {} derniers où les deux équipes ont marqué".format(self.success, self.total)
            if self.type.name == "CS":
                sentence = "{} clean sheets sur les {} derniers matchs".format(self.success, self.total)
            if self.type.name == "GS":
                sentence = "{} matchs sur les {} derniers où ils ont marqué au moins 1 but".format(self.success, self.total)
            if self.type.name == "GC":
                sentence = "{} matchs sur les {} derniers où ils ont encaissé au moins 1 but".format(self.success, self.total)
            if self.type.name == "p1_5":
                sentence = "{} des {} derniers matchs avec un total d'au moins de 2 buts ".format(self.success, self.total)
            if self.type.name == "m3_5":
                sentence = "{} des {} derniers matchs avec un total d'au plus de 3 buts ".format(self.success, self.total)
            if self.type.name == "TGS":
                sentence = "Total de {} buts marqués lors des {} derniers matchs".format(self.success, self.total)
            if self.type.name == "TGC":
                sentence = "Total de {} buts encaissés lors des {} derniers matchs".format(self.success, self.total)
            
        return "{} {} {}".format(prefixe, sentence, suffixe)


class BeforeMatchStat(BaseModel):   
    match                           = models.ForeignKey("fixtureApp.Match", on_delete = models.CASCADE, related_name="before_stat_match")
    team                            = models.ForeignKey("teamApp.EditionTeam", null = True, blank=True, on_delete = models.CASCADE, related_name="team_stat_match")
    ppg                             = models.FloatField(null = True, blank=True)
    points                          = models.FloatField(null = True, blank=True)
    goals_scored                    = models.IntegerField(null = True, blank=True)
    goals_conceded                  = models.IntegerField(null = True, blank=True)
    avg_goals_scored                = models.FloatField(null = True, blank=True)
    avg_goals_conceded              = models.FloatField(null = True, blank=True)
    avg_fouls_for                   = models.FloatField(null = True, blank=True)
    avg_fouls_against               = models.FloatField(null = True, blank=True)
    nb_matchs_gt_avg_fouls          = models.FloatField(null = True, blank=True)
    avg_corners_for                 = models.FloatField(null = True, blank=True)
    avg_corners_against             = models.FloatField(null = True, blank=True)
    nb_corners_gt_avg_fouls         = models.FloatField(null = True, blank=True)
    avg_shots_for                   = models.FloatField(null = True, blank=True)
    avg_shots_against               = models.FloatField(null = True, blank=True)
    nb_shots_gt_avg_fouls           = models.FloatField(null = True, blank=True)
    avg_shots_target_for            = models.FloatField(null = True, blank=True)
    avg_shots_target_against        = models.FloatField(null = True, blank=True)
    nb_shots_target_gt_avg_fouls    = models.FloatField(null = True, blank=True)
    avg_offside_for                 = models.FloatField(null = True, blank=True)
    avg_offside_against             = models.FloatField(null = True, blank=True)
    nb_offside_gt_avg_fouls         = models.FloatField(null = True, blank=True)
    avg_cards_for                   = models.FloatField(null = True, blank=True)
    avg_cards_against               = models.FloatField(null = True, blank=True)
    nb_cards_gt_avg_fouls           = models.FloatField(null = True, blank=True)
    list_confrontations             = models.TextField(default = "[]", null = True, blank=True)
    list_similaires_ppg             = models.TextField(default = "[]", null = True, blank=True)
    list_similaires_ppg2            = models.TextField(default = "[]", null = True, blank=True)
    list_similaires_betting         = models.TextField(default = "[]", null = True, blank=True)
    list_intercepts                 = models.TextField(default = "[]", null = True, blank=True)

    def __str__(self):
        return str(self.match)
    
    def mise_a_jour(self):
        match = self.match                                                
        if self.points is None:
            self.points                     = self.team.fight_points(match)
            self.list_intercepts            = json.dumps([str(x.id) for x in match.similaires_intercepts(10)])
            self.list_confrontations        = json.dumps([str(x.id) for x in match.confrontations_directes(10)])
            self.list_similaires_ppg        = json.dumps([str(x.id) for x in match.similaires_ppg(10)])
            self.list_similaires_ppg2       = json.dumps([str(x.id) for x in match.similaires_ppg2(10)])
            self.list_similaires_betting    = json.dumps([str(x.id) for x in match.similaires_betting(10)])
            self.save()



class ResultMatch(BaseModel):
    match              = models.ForeignKey("fixtureApp.Match", on_delete = models.CASCADE, related_name="result_match")
    home_score        = models.IntegerField(default = 0, null = True, blank=True)
    away_score        = models.IntegerField(default = 0, null = True, blank=True)
    result            = models.CharField(max_length = 255, null = True, blank=True)
    home_half_score   = models.IntegerField(default = None, null = True, blank=True)
    away_half_score   = models.IntegerField(default = None, null = True, blank=True)
    result_half       = models.CharField(max_length = 255, null = True, blank=True)

    def __str__(self):
        return str(self.match)+"==>"+str(self.home_score)+"-"+str(self.away_score)
    
    
class ExtraInfosMatch(BaseModel):
    match                   = models.ForeignKey("fixtureApp.Match", on_delete = models.CASCADE, related_name="extra_info_match")
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




# @signals.pre_save(sender=BeforeMatchStat)
# def sighandler(instance, **kwargs):
#     match = instance.match                                                
#     if instance.points is None:
#         instance.points                     = instance.team.fight_points(match)
#         instance.list_intercepts            = json.dumps([str(x.id) for x in match.similaires_intercepts(10)])
#         instance.list_confrontations        = json.dumps([str(x.id) for x in match.confrontations_directes(10)])
#         instance.list_similaires_ppg        = json.dumps([str(x.id) for x in match.similaires_ppg(10)])
#         instance.list_similaires_ppg2       = json.dumps([str(x.id) for x in match.similaires_ppg2(10)])
#         instance.list_similaires_betting    = json.dumps([str(x.id) for x in match.similaires_betting(10)])
