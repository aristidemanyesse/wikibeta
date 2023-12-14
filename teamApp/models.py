from django.db import models
from django.db.models import Avg, Sum, Q
from coreApp.functions import cal_expecded_goal
from coreApp.models import BaseModel
from fixtureApp.models import Match
from datetime import datetime
import json

from statsApp.models import BeforeMatchStat

class Team(BaseModel):
    code    = models.CharField(max_length = 255, null = True, blank=True)
    name    = models.CharField(max_length = 255, null = True, blank=True)
    name2   = models.CharField(max_length = 255, null = True, blank=True)
    abr     = models.CharField(max_length = 10, null = True, blank=True)
    pays    = models.ForeignKey("competitionApp.Pays", on_delete = models.CASCADE, related_name="pays_du_team")
    color1  = models.CharField(max_length = 255, default="", null = True, blank=True)
    color2  = models.CharField(max_length = 255, default="", null = True, blank=True)
    logo    = models.ImageField(max_length = 255, upload_to = "images/teams/", default="images/teams/default.png", null = True, blank=True)
    
    class Meta:
        ordering = ['name']




class EditionTeam(BaseModel):
    NB = 5
    edition   = models.ForeignKey("competitionApp.EditionCompetition", on_delete = models.CASCADE, related_name="edition_team")
    team      = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="team_edition")

    class Meta:
        ordering = ['team']
        
    def __str__(self):
        return str(self.team).replace("/", "_")
    
    
    def form(self, match):
        if self.team in [match.home.team, match.away.team] :
            result = match.get_result()
            if result is not None:
                if result.result == "D":
                    return "N"
                elif result.result == "H":
                    return "V" if (match.home.team == self.team) else "D"
                elif result.result == "A":
                    return "V" if (match.away.team == self.team) else "D"
    
    
    def points_for_this_macth(self, match):
        if self.team in [match.home.team, match.away.team] :
            result = match.get_result()
            if result is not None:
                if result.result == "D":
                    return 1
                elif result.result == "H":
                    return 3 if (match.home.team == self.team) else 0
                elif result.result == "A":
                    return 3 if (match.away.team == self.team) else 0
        
        
        
        
    def prev_match(self, match, edition = False):
        matchs = Match.objects.filter((Q(home = self) | Q(away = self)), date__lt = match.date, is_finished = True).exclude(id = match.id).order_by("-date")
        if edition:
            matchs = matchs.filter(edition = match.edition)
        return matchs.first()
    


    def next_match(self, match, edition = False):
        matchs = Match.objects.filter((Q(home = self) | Q(away = self)), date__gt = match.date).exclude(id = match.id).order_by("-date")
        if edition:
            matchs = matchs.filter(edition = match.edition)
        return matchs.first()
    
    
      
    def get_last_matchs(self, match, number = None, edition = False, position = False):
        matchs = Match.objects.filter((Q(home = self) | Q(away = self)), date__lt = match.date, is_finished = True).exclude(id = match.id).order_by("-date")
        if edition:
            matchs = matchs.filter(edition = match.edition)
        if position:
            matchs = matchs.filter(home = self) if self == match.home else matchs.filter(away = self)
            
        return matchs[:EditionTeam.NB if number is None else number]
    
      
    def get_last_home_matchs(self, match, number = None, edition = False, position = False):
        matchs = Match.objects.filter(home = self, date__lt = match.date, is_finished = True).exclude(id = match.id).order_by("-date")
        if edition:
            matchs = matchs.filter(edition = match.edition)
        if position:
            matchs = matchs.filter(home = self) if self == match.home else matchs.filter(away = self)
            
        return matchs[:EditionTeam.NB if number is None else number]
      
      
    def get_last_away_matchs(self, match, number = None, edition = False, position = False):
        matchs = Match.objects.filter(home = self, date__lt = match.date, is_finished = True).exclude(id = match.id).order_by("-date")
        if edition:
            matchs = matchs.filter(edition = match.edition)
        if position:
            matchs = matchs.filter(away = self) if self == match.home else matchs.filter(away = self)
            
        return matchs[:EditionTeam.NB if number is None else number]
    
    

    def get_last_form(self, match, number = None, edition = False):
        matchs = self.get_last_matchs(match, number, edition)
        return [self.form(x) for x in matchs]
    
    
    
    def last_stats(self, match, number = None, edition = False):
        try:
            total = pts = scored =  conceded = 0
            matchs = self.get_last_matchs(match, number, edition)
            if len(matchs) == 0:
                return 0, 0, 0, 0, 0, 0
            
            for match in matchs:
                result = match.get_result()
                if result is not None:
                    total       += 1
                    pts         += self.points_for_this_macth(match) or 0
                    scored      += (result.home_score or 0) if match.home == self else (result.away_score or 0)
                    conceded    += (result.home_score or 0) if match.away == self else (result.away_score or 0)
                    
        except Exception as e:
            print("Error last_stats ::: for ", match, match.date,  e)
            
        return pts, round((pts / total), 2) if total > 0 else 0, scored, round((scored/total), 2) if total > 0 else 0, conceded, round((conceded/total), 2) if total > 0 else 0
    
        
        
        
    def elo_score(self, match):
        try:            
            self_previous_match = self.prev_match(match, edition = True)
            if self_previous_match is None:
                return 1500
            self_stats = self_previous_match.get_home_before_stats() if self == self_previous_match.home else self_previous_match.get_away_before_stats()
            
            result = self_previous_match.get_result()
            bon_off, bon_def = 0, 0
            if self == self_previous_match.home:
                if result.home_score > result.away_score:
                    res = 1
                elif result.home_score < result.away_score:
                    res = 0
                    bon_def = (result.away_score - result.home_score == 1)
                else:
                    res = 0.5
                bon_off = (result.home_score >= 3)
                
            elif self == self_previous_match.away:
                if result.home_score > result.away_score:
                    res = 0
                    bon_def = (result.home_score - result.away_score == 1)
                elif result.home_score < result.away_score:
                    res = 1
                else:
                    res = 0.5
                bon_off = (result.away_score >= 3)
                
            
            new_elo = self_stats.score_elo + BeforeMatchStat.SCORE_ELO_FACTOR * (res - self_stats.probabilite_elo)
            new_elo += (BeforeMatchStat.SCORE_ELO_FACTOR * 1/10) if bon_off else 0
            new_elo += (BeforeMatchStat.SCORE_ELO_FACTOR * 1/10) if bon_def else 0
            
            return new_elo
            
        except Exception as e:
            print("Error elo_score ::: for ", match, match.date,  e)
            
            
        
    def calcul_expected_goals(self, match):
        try:
            self_previous_match = self.prev_match(match, edition = True)
            if self_previous_match is None:
                return 1, 1 # gs et gs expected
            self_stats = self_previous_match.get_home_before_stats() if self == self_previous_match.home else self_previous_match.get_away_before_stats()
            auth_stats = self_previous_match.get_home_before_stats() if self != self_previous_match.home else self_previous_match.get_away_before_stats()
            result = self_previous_match.get_result()
            
            goal_scored = result.home_score if self == self_previous_match.home else result.away_score  
            gs = max(cal_expecded_goal(self_stats.gs_expected, goal_scored, self_stats.expected_goals), 0.1)
            
            goal_conceded = result.home_score if self != self_previous_match.home else result.away_score  
            ga = max(cal_expecded_goal(self_stats.ga_expected, goal_conceded, auth_stats.expected_goals), 0.1)
            
            return gs, ga
        
        except Exception as e:
            print("Error expected_goals ::: for ", match, match.date,  e)
        
        
        
        
    def extra_info_stats(self, match, number = None, edition = False):
        try:
            matchs = self.get_last_matchs(match, number, edition)
            total = 0
            datas = {}
            datas["avg_fouls_for"]          = 0
            datas["avg_shots_for"]          = 0
            datas["avg_shots_target_for"]   = 0
            datas["avg_corners_for"]        = 0
            datas["avg_offside_for"]        = 0
            datas["avg_cards_for"]          = 0
            
            datas["avg_fouls_against"]          = 0
            datas["avg_shots_against"]          = 0
            datas["avg_shots_target_against"]   = 0
            datas["avg_corners_against"]        = 0
            datas["avg_offside_against"]        = 0
            datas["avg_cards_against"]          = 0

            if len(matchs) > 0:
                for match in matchs:
                    info = match.get_extra_info_match()
                    if info is not None:
                        total                               += 1
                        datas["avg_fouls_for"]              += (info.home_fouls or 0) if match.home == self else (info.away_fouls or 0)
                        datas["avg_shots_for"]              += (info.home_shots or 0) if match.home == self else (info.away_shots or 0)
                        datas["avg_shots_target_for"]       += (info.home_shots_on_target or 0) if match.home == self else (info.away_shots_on_target or 0)
                        datas["avg_corners_for"]            += (info.home_corners or 0 )if match.home == self else (info.away_corners or 0)
                        datas["avg_offside_for"]            += (info.home_offsides or 0) if match.home == self else (info.away_offsides or 0)
                        datas["avg_cards_for"]              += (info.home_yellow_cards or 0) if match.home == self else (info.away_yellow_cards or 0)

                        datas["avg_fouls_against"]          += (info.home_fouls or 0) if match.away == self else (info.home_fouls or 0)
                        datas["avg_shots_against"]          += (info.home_shots or 0) if match.away == self else (info.home_shots or 0)
                        datas["avg_shots_target_against"]   += (info.home_shots_on_target or 0) if match.away == self else (info.home_shots_on_target or 0)
                        datas["avg_corners_against"]        += (info.home_corners or 0 )if match.away == self else (info.home_corners or 0)
                        datas["avg_offside_against"]        += (info.home_offsides or 0) if match.away == self else (info.home_offsides or 0)
                        datas["avg_cards_against"]          += (info.home_yellow_cards or 0) if match.away == self else (info.home_yellow_cards or 0)
            
                for key in datas.keys():
                    datas[key] = round(datas[key] / total, 2) if total > 0 else 0
                    
        except Exception as e:
            print("Error extra_info_stats ::: for ", match, match.date,  e)
            
        return datas

    
    
    
    def get_before_stats(self, match):
        return match.before_stat_match.filter(team = self).first()


    def get_extra_info(self, match):
        return match.extra_match.filter(team = self).first()

    def get_team_profile(self, match):
        return self.team_profile.filter(match = match).first()
    
    
    def dynamique(self, match, number = 6):
        part = 11.667 / 21
        base = suite_v = suite_n = 0
        for i, mat in enumerate(self.get_last_matchs(match, number = number, edition = True)):
            result = mat.get_result()
            if result.home_score == result.away_score:
                suite_v = 0
                suite_n += 1
                base += (part * (6 - i)) / (1.5 if suite_n > 0 else 2)
            elif ((result.home_score > result.away_score and mat.home == self) or (result.home_score < result.away_score and mat.away == self)) :
                base += part * (6 - i) if suite_v == 0 else part * 6
                suite_v += 1
            else:
                suite_v = suite_n = 0
        return min(20, max(0, round(base , 2)))




    def attaque(self, match, number = 6):
        part = 0.27
        serie = []
        for i, mat in enumerate(self.get_last_matchs(match, number = number, edition = True)):
            result = mat.get_result()
            serie.append(result.home_score if mat.home == self else result.away_score)
        
        total = 0
        series = 0
        for i, score in enumerate(serie):
            total += part * (6-i) * score  + (part if series == 1 else 0)
            series = 0 if score == 0 else 1
            
        return min(20, max(0, round(total , 2)))
        
        
    
    def defense(self, match, number = 6):
        part = 0.27
        serie = []
        for i, mat in enumerate(self.get_last_matchs(match, number = number, edition = True)):
            result = mat.get_result()
            serie.append(result.home_score if mat.home != self else result.away_score)
        
        total = 0
        series = 0
        for i, score in enumerate(serie):
            total += part * (6-i) * score  + (part if series == 1 else 0)
            series = 0 if score == 0 else 1
        return min(20, max(0, round(20 - total , 2)))     
        
    
    
    def maitrise(self, match, number = 6):
        total = 0
        serie = []
        results = []
        for i, mat in enumerate(self.get_last_matchs(match, number = number, edition = True)):
            result = mat.get_result()
            serie.append(result.home_score if mat.home != self else result.away_score)
            results.append(1 if ((result.home_score > result.away_score and mat.home == self) or (result.home_score < result.away_score and mat.away == self)) else 0 if result.home_score == result.away_score else -1)
        
        if len(serie) > 0:
            part = 0.5
            series = 1 if serie[0] == 0 else 0
            for i, score in enumerate(serie):
                if score <= 2:
                    part = part / (score+1)
                    total += part + ((6-i) * part  if series == 1 else 0)
                    series = 1 if score == 0 else 0

                    
            series = 1 if results[0] != -1 else 0
            for i, res in enumerate(results):
                if res == 1:
                    part = 0.28
                    total += part + ((6-i) * part if series == 1 else 0)
                    series = 0 if res == -1 else 1
                elif res == 0:
                    part = 0.14
                    total += part + ((6-i) * part if series == 1 else 0)
                    series = 0 if res == -1 else 1
        return min(20, max(0, round(total , 2)))



    
    def plus_but(self, nb, date = datetime.today()):
        matchs = Match.objects.filter(is_finished = True, date__lt = date).exclude(is_posted = True).filter(Q(home = self) | Q(away = self))
        total = 0
        for match in matchs:
            result = match.get_result()
            if result is None:
                continue
            if result.home_score + result.away_score > nb:
                total += 1
        return total


    def moins_but(self, nb, date = datetime.today()):
        matchs = Match.objects.filter(is_finished = True, date__lt = date).exclude(is_posted = True).filter(Q(home = self) | Q(away = self))
        total = 0
        for match in matchs:
            result = match.get_result()
            if result is None:
                continue
            if result.home_score + result.away_score < nb:
                total += 1
        return total
    
    
    def ht_plus_but(self, nb, date = datetime.today()):
        matchs = Match.objects.filter(is_finished = True, date__lt = date).exclude(is_posted = True).filter(Q(home = self) | Q(away = self))
        total = 0
        for match in matchs:
            result = match.get_result()
            if result is None:
                continue
            if result.home_half_score is not None :
                if result.home_half_score + result.away_half_score > nb:
                    total += 1
        return total


    def ht_moins_but(self, nb, date = datetime.today()):
        matchs = Match.objects.filter(is_finished = True, date__lt = date).exclude(is_posted = True).filter(Q(home = self) | Q(away = self))
        total = 0
        for match in matchs:
            result = match.get_result()
            if result is None:
                continue
            if result.home_half_score is not None :
                if result.home_half_score + result.away_half_score < nb:
                    total += 1
        return total
    
    
    
