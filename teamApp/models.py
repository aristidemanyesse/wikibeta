from django.db import models
from django.db.models import Avg, Sum, Q
from coreApp.models import BaseModel
from fixtureApp.models import Match

    
class Team(BaseModel):
    name    = models.CharField(max_length = 255, null = True, blank=True)
    code    = models.CharField(max_length = 255, null = True, blank=True)
    pays    = models.ForeignKey("competitionApp.Pays", on_delete = models.CASCADE, related_name="pays_du_team")
    logo    = models.ImageField(max_length = 255, upload_to = "static/images/teams/", default="", null = True, blank=True)
    
    class Meta:
        ordering = ['name']




class EditionTeam(BaseModel):
    NB = 5
    edition   = models.ForeignKey("competitionApp.EditionCompetition", on_delete = models.CASCADE, related_name="edition_team")
    team      = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="team_edition")

    class Meta:
        ordering = ['team']
        
    def __str__(self):
        return str(self.team)
    
    
    def form(self, match):
        if self in [match.home, match.away] :
            result = match.get_result()
            if result is not None:
                if result.result == "D":
                    return "N"
                elif result.result == "H":
                    return "V" if (match.home == self) else "D"
                elif result.result == "A":
                    return "V" if (match.away == self) else "D"
    
    
    def points_for_this_macth(self, match):
        if self in [match.home, match.away] :
            result = match.get_result()
            if result is not None:
                if result.result == "D":
                    return 1
                elif result.result == "H":
                    return 3 if (match.home == self) else 0
                elif result.result == "A":
                    return 3 if (match.away == self) else 0
        
        
        
        
    def get_last_matchs(self, match, number = None, edition = False):
        matchs = Match.objects.filter((Q(home = self) | Q(away = self)), date__lt = match.date, is_finished = True).exclude(id = match.id).order_by("-date")
        if edition:
            matchs = matchs.filter(edition = match.edition)
        return matchs[:EditionTeam.NB if number is None else number]
    

    def get_last_form(self, match, number = None, edition = False):
        matchs = self.get_last_matchs(match, number, edition)
        return [self.form(x) for x in matchs]
    
    
    def last_stats(self, match, number = None, edition = False):
        total = points = scored =  conceded = 0
        matchs = self.get_last_matchs(match, number, edition)
        if len(matchs) == 0:
            return 0, 0, 0, 0, 0, 0
        
        for match in matchs:
            result = match.get_result()
            if result is not None:
                total       += 1
                points      += self.points_for_this_macth(match) or 0
                scored      += (result.home_score or 0) if match.home == self else (result.away_score or 0)
                conceded    += (result.home_score or 0) if match.away == self else (result.away_score or 0)
        
        return points, round((points / total), 2) if total > 0 else 0, scored, round((scored/total), 2) if total > 0 else 0, conceded, round((conceded/total), 2) if total > 0 else 0
    


    def extra_info_stats(self, match, number = None, edition = False):
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
                    total             += 1
                    datas["avg_fouls_for"]          += (info.home_fouls or 0) if match.home == self else (info.away_fouls or 0)
                    datas["avg_shots_for"]          += (info.home_shots or 0) if match.home == self else (info.away_shots or 0)
                    datas["avg_shots_target_for"]   += (info.home_shots_on_target or 0) if match.home == self else (info.away_shots_on_target or 0)
                    datas["avg_corners_for"]        += (info.home_corners or 0 )if match.home == self else (info.away_corners or 0)
                    datas["avg_offside_for"]        += (info.home_offsides or 0) if match.home == self else (info.away_offsides or 0)
                    datas["avg_cards_for"]          += (info.home_yellow_cards or 0) if match.home == self else (info.away_yellow_cards or 0)

                    datas["avg_fouls_against"]          += (info.home_fouls or 0) if match.away == self else (info.home_fouls or 0)
                    datas["avg_shots_against"]          += (info.home_shots or 0) if match.away == self else (info.home_shots or 0)
                    datas["avg_shots_target_against"]   += (info.home_shots_on_target or 0) if match.away == self else (info.home_shots_on_target or 0)
                    datas["avg_corners_against"]        += (info.home_corners or 0 )if match.away == self else (info.home_corners or 0)
                    datas["avg_offside_against"]        += (info.home_offsides or 0) if match.away == self else (info.home_offsides or 0)
                    datas["avg_cards_against"]          += (info.home_yellow_cards or 0) if match.away == self else (info.home_yellow_cards or 0)
        
            for key in datas.keys():
                datas[key] = round(datas[key] / total, 2) if total > 0 else 0
            
        return datas

    
    
    
    def get_before_stats(self, match):
        return match.before_stat_match.filter(team = self).first()


    def get_extra_info(self, match):
        return match.extra_match.filter(team = self).first()



    
    def plus_but(self, nb):
        matchs = Match.objects.filter(is_finished = True).filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_score + result.away_score > nb:
                total += 1
        return total


    def moins_but(self, nb):
        matchs = Match.objects.filter(is_finished = True).filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_score + result.away_score < nb:
                total += 1
        return total
    
    
    def ht_plus_but(self, nb):
        matchs = Match.objects.filter(is_finished = True).filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_half_score is not None :
                if result.home_half_score + result.away_half_score > nb:
                    total += 1
        return total


    def ht_moins_but(self, nb):
        matchs = Match.objects.filter(is_finished = True).filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_half_score is not None :
                if result.home_half_score + result.away_half_score < nb:
                    total += 1
        return total
    
    
    
    
    