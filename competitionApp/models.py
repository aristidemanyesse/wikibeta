from django.db import models
from django.db.models import  Q
from coreApp.models import BaseModel
from coreApp.functions import *
from fixtureApp.models import *
from bettingApp.models import *
from teamApp.models import *


class Pays(BaseModel):
    code    = models.CharField(max_length = 255, null = True, blank=True)
    name    = models.CharField(max_length = 255, null = True, blank=True)
    abr    = models.CharField(max_length = 255, null = True, blank=True)
    flag    = models.ImageField(max_length = 255, upload_to = "static/images/pays/", default="", null = True, blank=True)

    class Meta:
        ordering = ['name']


class TypeCompetition(BaseModel):
    name    = models.CharField(max_length = 255, null = True, blank=True)
        

class Competition(BaseModel):
    identifiant   = models.CharField(max_length = 255, default="", null = True, blank=True)
    name          = models.CharField(max_length = 255, default="", null = True, blank=True)
    code          = models.CharField(max_length = 255, default="", null = True, blank=True)
    pays          = models.ForeignKey(Pays, on_delete = models.CASCADE, null = True, blank=True, related_name="pays_de_competition")
    logo          = models.ImageField(max_length = 255, upload_to = "static/images/competitions/", default="", null = True, blank=True)
    type          = models.ForeignKey(TypeCompetition, on_delete = models.CASCADE, null = True, blank=True, related_name="type_de_competition")
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name


class Edition(BaseModel):
    name          = models.CharField(max_length = 255, null = True, blank=True)
    
    class Meta:
        ordering = ['-name']
        
    def next(self):
        if len(self.name) > 5:
            t = self.name.split("-")
            return "{}-{}".format(int(t[0])+1, int(t[1])+1)
        else:
            return "{}".format(int(self.name)+1)
        
        
        

class EditionCompetition(BaseModel):
    edition       = models.ForeignKey(Edition, on_delete = models.CASCADE, related_name="edition_team")
    competition   = models.ForeignKey(Competition, on_delete = models.CASCADE, related_name="competition_edition")
    start_date    = models.DateField(null = True, blank=True)
    finish_date   = models.DateField(null = True, blank=True)
    is_finished   = models.BooleanField(default=False, null = True, blank=True)

    class Meta:
        ordering = ["competition", '-start_date']

    def __str__(self):
        return str(self.competition) +" - "+ str(self.edition)
    
    
    def classement(self, date):
        datas = []
        for team in self.edition_team.filter():
            cs = btts = ga = gs = 0
            win = draw = lose = 0
            matchs = Match.objects.filter(is_finished = True, date__lte = date).filter(Q(home = team) | Q(away = team)).order_by("-date")
            if len(matchs) > 0:
                for match in matchs:
                    result = match.get_result()
                    if result is not None:
                        btts += 1 if (result.home_score > 0 and result.away_score > 0)  else 0
                        if match.home == team:
                            gs += result.home_score
                            ga += result.away_score
                            cs += 1 if result.away_score == 0 else 0
                        elif match.away == team:
                            gs += result.away_score
                            ga += result.home_score
                            cs += 1 if result.home_score == 0 else 0
                        if result.result == "D":
                            draw += 1
                        if (result.result == "H" and match.home == team) or (result.result == "A" and match.away == team ) :
                            win += 1
                        if (result.result == "A" and match.home == team) or (result.result == "H" and match.away == team ) :
                            lose += 1
                                                
                pts = win*3 + draw
                ppg = round(pts / len(matchs), 2)
                avg_gs = round(gs / len(matchs), 2)
                avg_ga = round(ga / len(matchs), 2)
                
                element = {
                    "team"    : team,
                    "mj"      : len(matchs),
                    "win"     : win,
                    "draw"    : draw,
                    "lose"    : lose,
                    "gs"      : gs,
                    "ga"      : ga,
                    "gd"      : gs - ga,
                    "form"     : [team.form(x) for x in matchs[:EditionTeam.NB]],
                    "pts"     : pts,
                    "ppg"     : ppg,
                    "cs"      : cs,
                    "btts"    : btts,
                    "avg_gs"  : avg_gs,
                    "avg_ga"  : avg_ga,
                    "p1_5"    : int(round(team.plus_but(1.5)/len(matchs), 2)*100),
                    "p2_5"    : int(round(team.plus_but(2.5)/len(matchs), 2)*100),
                    "m3_5"    : int(round(team.moins_but(3.5)/len(matchs), 2)*100),
                }
                element["form"].reverse()
                datas.append(element)
        
        datas = sorted(datas, reverse=True, key=lambda x: (x.get("pts"), x.get("gd"), x.get("win")))
        return datas
    
    
    
    
    def cs(self):
        matchs = self.edition_du_match.filter(is_finished = True)
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_score == 0 or  result.away_score == 0:
                total +=1
        return total
    
    def half_cs(self):
        matchs = self.edition_du_match.filter(is_finished = True)
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_half_score is not None:
                if result.home_half_score == 0 or result.away_half_score == 0:
                    total +=1
        return total


    def btts(self):
        matchs = self.edition_du_match.filter(is_finished = True)
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_score > 0 and result.away_score > 0:
                total +=1
        return total
    
    
    def half_btts(self):
        matchs = self.edition_du_match.filter(is_finished = True)
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_half_score is not None:
                if result.home_half_score > 0 and  result.away_half_score > 0:
                    total +=1
        return total
    

    def nul_nul(self):
        matchs = self.edition_du_match.filter(is_finished = True)
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_score == 0 and result.away_score == 0:
                total +=1
        return total
    
    
    def half_nul_nul(self):
        matchs = self.edition_du_match.filter(is_finished = True)
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_half_score is not None:
                if result.home_half_score == 0 and  result.away_half_score == 0:
                    total +=1
        return total
    
    
    
    def avg_buts(self):
        matchs = self.edition_du_match.filter(is_finished = True)
        total = 0
        for match in matchs:
            result = match.get_result()
            total += result.home_score + result.away_score
        return round(total / len(matchs), 2) if len(matchs) > 0 else 0
    
    
    def half_avg_buts(self):
        matchs = self.edition_du_match.filter(is_finished = True)
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_half_score is not None:
                total += result.home_half_score + result.away_half_score
        return round(total / len(matchs), 2) if len(matchs) > 0 else 0
    
    
    def second_avg_buts(self):
        matchs = self.edition_du_match.filter(is_finished = True)
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_half_score is not None:
                total += result.home_score  - result.home_half_score + result.away_score - result.away_half_score
        return round(total / len(matchs), 2) if len(matchs) > 0 else 0
    
        
                
    def plus_but(self, nb):
        matchs = self.edition_du_match.filter(is_finished = True)
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_score + result.away_score > nb:
                total += 1
        return total


    def moins_but(self, nb):
        matchs = self.edition_du_match.filter(is_finished = True)
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_score + result.away_score < nb:
                total += 1
        return total
    
    
    def ht_plus_but(self, nb):
        matchs = self.edition_du_match.filter(is_finished = True)
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_half_score is not None :
                if result.home_half_score + result.away_half_score > nb:
                    total += 1
        return total


    def ht_moins_but(self, nb):
        matchs = self.edition_du_match.filter(is_finished = True)
        total = 0
        for match in matchs:
            result = match.get_result()
            if result.home_half_score is not None :
                if result.home_half_score + result.away_half_score < nb:
                    total += 1
        return total
    
    
    

class Ranking(BaseModel):
    date              = models.DateField( null = True, blank=True)
    edition       = models.ForeignKey(EditionCompetition, on_delete = models.CASCADE, related_name="edition_rankings")

    def __str__(self):
        return str(self.edition)
    
        
class LigneRanking(BaseModel):
    ranking   = models.ForeignKey(Ranking, on_delete = models.CASCADE, related_name="ranking_lignes")
    team      = models.ForeignKey(EditionTeam, on_delete = models.CASCADE, related_name="team_lignes_rankings")
    level     = models.IntegerField(default= 0, null = True, blank=True)
    mj        = models.IntegerField(default= 0, null = True, blank=True)
    win       = models.IntegerField(default= 0, null = True, blank=True)
    draw      = models.IntegerField(default= 0, null = True, blank=True)
    lose      = models.IntegerField(default= 0, null = True, blank=True)
    gs        = models.IntegerField(default= 0, null = True, blank=True)
    ga        = models.IntegerField(default= 0, null = True, blank=True)
    gd        = models.IntegerField(default= 0, null = True, blank=True)
    form      = models.CharField(max_length=255, default= "", null = True, blank=True)
    ppg       = models.FloatField(default = 0.0, null = True, blank=True)
    pts       = models.IntegerField(default= 0, null = True, blank=True)
    cs        = models.IntegerField(default= 0, null = True, blank=True)
    btts      = models.IntegerField(default= 0, null = True, blank=True)
    avg_gs    = models.FloatField(default = 0.0, null = True, blank=True)
    avg_ga    = models.FloatField(default = 0.0, null = True, blank=True)
    p1_5      = models.FloatField(default = 0.0, null = True, blank=True)
    p2_5      = models.FloatField(default = 0.0, null = True, blank=True)
    m3_5      = models.FloatField(default = 0.0, null = True, blank=True)
    
    class Meta:
        ordering = ['level']

    def __str__(self):
        return "Rang - " + str(self.team)
    
    

class CompetitionStat(BaseModel):   
    edition             = models.ForeignKey(EditionCompetition, null = True, blank=True, on_delete = models.CASCADE, related_name="edition_stats")
    ranking             = models.ForeignKey(Ranking, null = True, blank=True, on_delete = models.CASCADE, related_name="ranking_stats")
    avg_goals           = models.FloatField(null = True, blank=True)
    avg_fouls           = models.FloatField(null = True, blank=True)
    avg_corners         = models.FloatField(null = True, blank=True)
    avg_shots           = models.FloatField(null = True, blank=True)
    avg_shots_target    = models.FloatField(null = True, blank=True)
    avg_offside         = models.FloatField(null = True, blank=True)
    avg_yellow_cards    = models.FloatField(null = True, blank=True)
    avg_red_cards       = models.FloatField(null = True, blank=True)

    def __str__(self):
        return "Stats de "+str(self.edition)
