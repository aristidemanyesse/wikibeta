from django.db import models
from django.db.models import Avg, Sum, Q
from core.models import BaseModel, Etat
from django.core.validators import MinValueValidator
from fractions import Fraction
from core.functions import *

class Pays(BaseModel):
    name    = models.CharField(max_length = 255, null = True, blank=True)
    code    = models.CharField(max_length = 255, null = True, blank=True)
    flag    = models.ImageField(max_length = 255, upload_to = "static/images/pays/", default="", null = True, blank=True)

    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name


class Competition(BaseModel):
    name    = models.CharField(max_length = 255, null = True, blank=True)
    code    = models.CharField(max_length = 255, null = True, blank=True)
    pays    = models.ForeignKey(Pays, on_delete = models.CASCADE, related_name="pays_de_competition")

    def __str__(self):
        return self.name


class Edition(BaseModel):
    name          = models.CharField(max_length = 255, null = True, blank=True)
    
    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name

class EditionCompetition(BaseModel):
    edition       = models.ForeignKey(Edition, on_delete = models.CASCADE, related_name="edition_team")
    competition   = models.ForeignKey(Competition, on_delete = models.CASCADE, related_name="competition_edition")
    start_date    = models.DateField(null = True, blank=True)
    finish_date   = models.DateField(null = True, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return str(self.competition) +" - "+ str(self.edition)
    
    
    def classement(self):
        datas = []
        for team in self.edition_team.filter():
            cs = btts = ga = gs = 0
            matchs = Match.objects.filter(Q(home = team) | Q(away = team)).order_by("-date")
            for match in matchs:
                btts += 1 if (match.home_score > 0 and match.away_score > 0)  else 0
                if match.home == team:
                    gs += match.home_score
                    ga += match.away_score
                    cs += 1 if match.away_score == 0 else 0
                elif match.away == team:
                    gs += match.away_score
                    ga += match.home_score
                    cs += 1 if match.home_score == 0 else 0
            win = Match.objects.filter(Q(home = team , result = "H") | Q(away = team , result = "A"))
            draw = Match.objects.filter(Q(home = team , result = "D") | Q(away = team , result = "D"))
            lose = Match.objects.filter(Q(home = team , result = "A") | Q(away = team , result = "H"))
            pts = len(win)*3 + len(draw)
            ppg = round(pts / len(matchs), 2)
            avg_gs = round(gs / len(matchs), 2)
            
            element = {
                "team"    : team,
                "mj"      : len(matchs),
                "win"     : len(win),
                "draw"    : len(draw),
                "lose"    : len(lose),
                "gs"      : gs,
                "ga"      : ga,
                "gd"      : gs - ga,
                "form"     : [x.form(team) for x in matchs[:EditionTeam.NB]],
                "pts"     : pts,
                "ppg"     : ppg,
                "cs"      : cs,
                "btts"    : btts,
                "avg_gs"  : avg_gs,
                "btts"    : btts,
                "1.5"    : int(round(team.plus_but(1.5)/len(matchs), 2)*100),
                "2.5"    : int(round(team.plus_but(2.5)/len(matchs), 2)*100),
                "3.5"    : int(round(team.moins_but(3.5)/len(matchs), 2)*100),
            }
            element["form"].reverse()
            datas.append(element)
        
        datas = sorted(datas, reverse=True, key=lambda x: x.get("pts"))
        return datas
    
    
    def cs(self):
        matchs = self.edition_du_match.filter()
        total = 0
        for match in matchs:
            if match.home_score == 0 or  match.away_score == 0:
                total +=1
        return total
    
    def half_cs(self):
        matchs = self.edition_du_match.filter()
        total = 0
        for match in matchs:
            if match.home_half_score is not None:
                if match.home_half_score == 0 or match.away_half_score == 0:
                    total +=1
        return total


    def btts(self):
        matchs = self.edition_du_match.filter()
        total = 0
        for match in matchs:
            if match.home_score > 0 and match.away_score > 0:
                total +=1
        return total
    
    
    def half_btts(self):
        matchs = self.edition_du_match.filter()
        total = 0
        for match in matchs:
            if match.home_half_score is not None:
                if match.home_half_score > 0 and  match.away_half_score > 0:
                    total +=1
        return total
    

    def nul_nul(self):
        matchs = self.edition_du_match.filter()
        total = 0
        for match in matchs:
            if match.home_score == 0 and match.away_score == 0:
                total +=1
        return total
    
    
    def half_nul_nul(self):
        matchs = self.edition_du_match.filter()
        total = 0
        for match in matchs:
            if match.home_half_score is not None:
                if match.home_half_score == 0 and  match.away_half_score == 0:
                    total +=1
        return total
    
    
    
    def avg_buts(self):
        matchs = self.edition_du_match.filter()
        total = 0
        for match in matchs:
            total += match.home_score + match.away_score
        return round(total / len(matchs), 2) if len(matchs) > 0 else 0
    
    
    def half_avg_buts(self):
        matchs = self.edition_du_match.filter()
        total = 0
        for match in matchs:
            if match.home_half_score is not None:
                total += match.home_half_score + match.away_half_score
        return round(total / len(matchs), 2) if len(matchs) > 0 else 0
    
    
    def second_avg_buts(self):
        matchs = self.edition_du_match.filter()
        total = 0
        for match in matchs:
            if match.home_half_score is not None:
                total += match.home_score  - match.home_half_score + match.away_score - match.away_half_score
        return round(total / len(matchs), 2) if len(matchs) > 0 else 0
    
        
                
    def plus_but(self, nb):
        matchs = self.edition_du_match.filter()
        total = 0
        for match in matchs:
            if match.home_score + match.away_score > nb:
                total += 1
        return total


    def moins_but(self, nb):
        matchs = self.edition_du_match.filter()
        total = 0
        for match in matchs:
            if match.home_score + match.away_score < nb:
                total += 1
        return total
    
    
    def ht_plus_but(self, nb):
        matchs = self.edition_du_match.filter()
        total = 0
        for match in matchs:
            if match.home_half_score is not None :
                if match.home_half_score + match.away_half_score > nb:
                    total += 1
        return total


    def ht_moins_but(self, nb):
        matchs = self.edition_du_match.filter()
        total = 0
        for match in matchs:
            if match.home_half_score is not None :
                if match.home_half_score + match.away_half_score < nb:
                    total += 1
        return total
    
    
    
    
    
    
    
class Team(BaseModel):
    name    = models.CharField(max_length = 255, null = True, blank=True)
    code    = models.CharField(max_length = 255, null = True, blank=True)
    pays    = models.ForeignKey(Pays, on_delete = models.CASCADE, related_name="pays_du_team")
    logo    = models.ImageField(max_length = 255, upload_to = "static/images/team/", default="", null = True, blank=True)
    
    def __str__(self):
        return self.name





class EditionTeam(BaseModel):
    NB = 10
    edition   = models.ForeignKey(EditionCompetition, on_delete = models.CASCADE, related_name="edition_team")
    team      = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="team_edition")

    class Meta:
        ordering = ['-edition']
        
    def __str__(self):
        return str(self.team)
    
    
    
    def get_last_matchs(self):
        # request.session['match'] = match
        matchs = self.edition.edition_du_match.filter(Q(home = self) | Q(away = self)).order_by("-date")
        return matchs[:EditionTeam.NB]
    
    def get_last_form(self):
        matchs = self.get_last_matchs()
        return [x.form(self) for x in matchs[:EditionTeam.NB]]
    
    
    def plus_but(self, nb):
        matchs = Match.objects.filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            if match.home_score + match.away_score > nb:
                total += 1
        return total


    def moins_but(self, nb):
        matchs = Match.objects.filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            if match.home_score + match.away_score < nb:
                total += 1
        return total
    
    
    def ht_plus_but(self, nb):
        matchs = Match.objects.filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            if match.home_half_score is not None :
                if match.home_half_score + match.away_half_score > nb:
                    total += 1
        return total


    def ht_moins_but(self, nb):
        matchs = Match.objects.filter(Q(home = self) | Q(away = self)).order_by("-date")
        total = 0
        for match in matchs:
            if match.home_half_score is not None :
                if match.home_half_score + match.away_half_score < nb:
                    total += 1
        return total
    
    
    
    
    
    
class Match(BaseModel):
    date              = models.DateField( null = True, blank=True)
    home              = models.ForeignKey(EditionTeam, on_delete = models.CASCADE, related_name="home_match")
    away              = models.ForeignKey(EditionTeam, on_delete = models.CASCADE, related_name="away_match")
    home_score        = models.IntegerField(default = 0, null = True, blank=True)
    away_score        = models.IntegerField(default = 0, null = True, blank=True)
    result            = models.CharField(max_length = 255, null = True, blank=True)
    home_half_score   = models.IntegerField(default = 0, null = True, blank=True)
    away_half_score   = models.IntegerField(default = 0, null = True, blank=True)
    result_half       = models.CharField(max_length = 255, null = True, blank=True)
    edition           = models.ForeignKey(EditionCompetition, on_delete = models.CASCADE, related_name="edition_du_match")
    is_finished        = models.BooleanField(default = False, null = True, blank=True)


    class Meta:
        ordering = ['date']
     

    def __str__(self):
        return str(self.home) +" -VS- "+ str(self.away)


    def score(self):
        return str(self.home_score) +" - "+ str(self.away_score)
       
    
    def confrontations_directes(self):
        matchs = Match.objects.filter(Q(home__team = self.home.team, away__team = self.away.team) | Q(home__team = self.away.team,  away__team = self.home.team)).filter(date__lte = self.date).exclude(id = self.id).order_by("-date")        
        return matchs[:EditionTeam.NB]
    
    
    def similaires_ppg(self):
        matchs = []
        total = 0
        ppg_home = self.before_stat_match.filter(team = self.home).first().ppg
        ppg_away = self.before_stat_match.filter(team = self.away).first().ppg
        
        befores = BeforeMatchStat.objects.filter(ppg__range = intervale(ppg_home)).filter(match__date__lte = self.date).exclude(id = self.id)
        print(len(befores))
        datas = [bef for bef in befores if bef.team == bef.match.home ]
        print(len(datas))
        exit()
        print("**//////////////////////////", len(matchs))
        return matchs
        # return matchs[:EditionTeam.NB]
    
    
    def form(self, team : EditionTeam):
        if team == self.home or team == self.away:
            if self.result == "D":
                return "N"
            elif self.result == "H":
                return "V" if (self.home == team) else "D"
            elif self.result == "A":
                return "V" if (self.away == team) else "D"
        return ""
    
    
    def points_for_this_macth(self, team : EditionTeam):
        if team == self.home or team == self.away:
            if self.result == "D":
                return 1
            elif self.result == "H":
                return 3 if (self.home == team) else 0
            elif self.result == "A":
                return 3 if (self.away == team) else 0
        return 0
        
        
    def goals_scored(self, team : EditionTeam):
        if team == self.home or team == self.away:
            return self.home_score if self.home == team else self.away_score
        return 0
    

    def goals_conceded(self, team : EditionTeam):
        if team == self.home or team == self.away:
            return self.away_score if self.home == team else self.home_score
        return 0
       

    def get_home_before_stats(self):
        return self.before_stat_match.filter(team = self.home).first()

    def get_away_before_stats(self):
        return self.before_stat_match.filter(team = self.away).first()  

    def get_home_extra_info(self):
        return self.extra_match.filter(team = self.home).first()

    def get_away_extra_info(self):
        return self.extra_match.filter(team = self.away).first()

    def get_bet365(self):
        return self.match_odds.filter(booker__code = "B365").first()
    
    
class BeforeMatchStat(BaseModel):   
    match               = models.ForeignKey(Match, on_delete = models.CASCADE, related_name="before_stat_match")
    team                = models.ForeignKey(EditionTeam, null = True, blank=True, on_delete = models.CASCADE, related_name="team_stat_match")
    ppg                 = models.FloatField(null = True, blank=True)
    goals_scored        = models.FloatField(null = True, blank=True)
    avg_goals_scored    = models.FloatField(null = True, blank=True)
    goals_conceded      = models.FloatField(null = True, blank=True)
    avg_goals_conceded  = models.FloatField(null = True, blank=True)

    def __str__(self):
        return str(self.match)



class ExtraInfosMatch(BaseModel):
    match                   = models.ForeignKey(Match, on_delete = models.CASCADE, related_name="extra_match")
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
    
    
class Goal(BaseModel):
    match             = models.ForeignKey(Match, on_delete = models.CASCADE, related_name="goal_du_match")
    team              = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="team_du_goal")
    minute            = models.CharField(max_length = 255, null = True, blank=True)
    is_penalty        = models.BooleanField(default = False, null = True, blank=True)
    home_half_score   = models.IntegerField(default = 0, null = True, blank=True)
    away_half_score   = models.IntegerField(default = 0, null = True, blank=True)

    def __str__(self):
        return str(self.team) +" goal in "+ str(self.match)


