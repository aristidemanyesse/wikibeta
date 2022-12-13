from django.db import models
from django.db.models import Avg, Sum, Q
from coreApp.models import BaseModel
from coreApp.functions import *
import fixtureApp.models

    
class Team(BaseModel):
    name    = models.CharField(max_length = 255, null = True, blank=True)
    code    = models.CharField(max_length = 255, null = True, blank=True)
    pays    = models.ForeignKey("competitionApp.Pays", on_delete = models.CASCADE, related_name="pays_du_team")
    logo    = models.ImageField(max_length = 255, upload_to = "static/images/team/", default="", null = True, blank=True)
    
    def __str__(self):
        return self.name




class EditionTeam(BaseModel):
    NB = 7
    edition   = models.ForeignKey("competitionApp.EditionCompetition", on_delete = models.CASCADE, related_name="edition_team")
    team      = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="team_edition")

    class Meta:
        ordering = ['-edition']
        
    def __str__(self):
        return str(self.team)
    
    
    def form(self, match):
        if self in [match.home, match.away] :
            if match.get_result().result == "D":
                return "N"
            elif match.get_result().result == "H":
                return "V" if (match.home == self) else "D"
            elif match.get_result().result == "A":
                return "V" if (match.away == self) else "D"
    
    
    def points_for_this_macth(self, match):
        if self in [match.home, match.away] :
            if match.get_result().result == "D":
                return 1
            elif match.get_result().result == "H":
                return 3 if (match.home == self) else 0
            elif match.get_result().result == "A":
                return 3 if (match.away == self) else 0
        return 0
        
        
        
        
    def get_last_matchs(self, match, number = None, edition = False):
        matchs = fixtureApp.models.Match.objects.filter(date__lt = match.date).filter(Q(home = self) | Q(away = self)).order_by("-date")
        if edition:
            matchs = matchs.filter(edition = match.edition)
        return matchs[:EditionTeam.NB if number is None else number]
    

    def get_last_form(self, match, number = None, edition = False):
        matchs = self.get_last_matchs(match, number, edition)
        return [x.form(self) for x in matchs]
    
    
    def last_stats(self, match, number = None, edition = False):
        points = scored =  conceded = 0
        matchs = self.get_last_matchs(match, number, edition)
        if len(matchs) ==0:
            return 0, 0, 0, 0, 0, 0
        for match in matchs:
            points    += self.points_for_this_macth(match)
            scored    += match.get_result().home_score if match.home == self else match.get_result().away_score
            conceded  += match.get_result().home_score if match.away == self else match.get_result().away_score
        
        return points, round(points / len(matchs)), scored, scored/len(matchs), conceded, conceded/len(matchs)
    

    
    
    def get_before_stats(self, match):
        return match.before_stat_match.filter(team = self).first()


    def get_extra_info(self, match):
        return match.extra_match.filter(team = self).first()



    
    def plus_but(self, nb):
        matchs = fixtureApp.models.Match.objects.filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            if match.get_result().home_score + match.get_result().away_score > nb:
                total += 1
        return total


    def moins_but(self, nb):
        matchs = fixtureApp.models.Match.objects.filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            if match.get_result().home_score + match.get_result().away_score < nb:
                total += 1
        return total
    
    
    def ht_plus_but(self, nb):
        matchs = fixtureApp.models.Match.objects.filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            if match.get_result().home_half_score is not None :
                if match.get_result().home_half_score + match.get_result().away_half_score > nb:
                    total += 1
        return total


    def ht_moins_but(self, nb):
        matchs = fixtureApp.models.Match.objects.filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            if match.get_result().home_half_score is not None :
                if match.get_result().home_half_score + match.get_result().away_half_score < nb:
                    total += 1
        return total
    
    
    
    
    