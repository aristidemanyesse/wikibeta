from math import sqrt
from competitionApp.models import *
from predictionApp.models import *

def predictscore(match):
    try:
        if len( match.away.get_last_matchs(match, edition = True)) < 4 or len( match.home.get_last_matchs(match, edition = True)) < 4:
            return []
        
        home = match.home.get_team_profile(match)
        away = match.away.get_team_profile(match)
        if home is None or away is None:
            return []
        
        home_stats = match.get_home_before_stats()
        away_stats = match.get_away_before_stats()
        compet =  match.edition.edition_stats.filter(ranking__date__lte = match.date).first()
        
        
        scores_exacts = []
        for i in range(0, 7):
            for j in range(0, 7):
                s = PredictionScore(
                    home_score = i,
                    away_score = j,
                )
                scores_exacts.append(s)
                
        
        scores_exacts = [ x for x in scores_exacts if x.home_score <= round(compet.avg_goals)+3 ]
        scores_exacts = [ x for x in scores_exacts if x.away_score <= round(compet.avg_goals)+2 ]
        scores_exacts = [ x for x in scores_exacts if abs(x.away_score - x.home_score) <= round(compet.avg_goals)*2 ]
        
        
        if max(home.attack, home.defense, home.dynamique, away.attack, away.defense, away.dynamique ) ==  away.defense:
            scores_exacts = [ x for x in scores_exacts if x.total() < 6.5 ]
        if max(home.attack, home.defense, home.dynamique, away.attack, away.defense, away.dynamique ) ==  home.defense:
            scores_exacts = [ x for x in scores_exacts if x.total() < 6.5 ]
            scores_exacts = [ x for x in scores_exacts if not x.home_score == x.away_score >=4 ]
        
        if (home.defense < 8 and away.defense < 7):
            scores_exacts = [ x for x in scores_exacts if x.total() >= 1 ]
        if (home.dynamique >= 12  and  away.defense <= 5):
            scores_exacts = [ x for x in scores_exacts if x.away_score <= x.home_score ]
        if (home.dynamique > 12):
            scores_exacts = [ x for x in scores_exacts if  x.away_score <= 3 ]
            
        scores_exacts = [ x for x in scores_exacts if  x.away_score <= home_stats.avg_goals_scored + 2 ]
        
        if (away.dynamique < 10):
            scores_exacts = [ x for x in scores_exacts if  x.away_score <= 3 ]
        if (away_stats.avg_goals_conceded > 2 or  home_stats.avg_goals_scored > 2):
            scores_exacts = [ x for x in scores_exacts if x.total() >= 1 ]
        if (home_stats.avg_goals_scored >= 2):
            scores_exacts = [ x for x in scores_exacts if x.total() >= 1 ]
        if (home_stats.avg_goals_scored >= 1.8 and away_stats.avg_goals_scored >= 1.8):
            scores_exacts = [ x for x in scores_exacts if x.total() >= 1 ]
            
        
        if (away_stats.avg_goals_conceded < 1 and home_stats.avg_goals_conceded < 1):
            scores_exacts = [ x for x in scores_exacts if x.total() < 5 ]
            
            
        x = scores_exacts[0]
        if x.total() == 0:
            scores_exacts = [ x for x in scores_exacts if x.total() < 5.5 ]
            scores_exacts = [ x for x in scores_exacts if x.home_score <= 3 and x.away_score <= 3 ]
            
            
        calcul = {"p1_5": 0,  "m3_5": 0, "home": 0, "away": 0, "nul":0, "cs": 0, "btts": 0}
        for x in scores_exacts:
            if x.home_score > x.away_score:
                calcul["home"] += 1
            if x.home_score < x.away_score:
                calcul["away"] += 1
            if x.home_score == x.away_score:
                calcul["nul"] += 1
            if x.total() > 2.5:
                calcul["p1_5"] += 1
            if x.total() < 2.5:
                calcul["m3_5"] += 1
            if x.home_score > 0 and x.away_score > 0:
                calcul["btts"] += 1
            else:
                calcul["cs"] += 1

            
        GF = 2.2
        before_home = match.home.get_before_stats(match)
        before_away = match.away.get_before_stats(match)
        home_u = sqrt(before_home.avg_goals_scored * before_away.avg_goals_conceded)
        away_u = sqrt(before_home.avg_goals_conceded * before_away.avg_goals_scored)
        
        if (before_home.avg_goals_scored + before_away.avg_goals_conceded + before_home.avg_goals_conceded + before_away.avg_goals_scored) / 4 > GF:
            scores_exacts = [ x for x in scores_exacts if x.total() >= 1]       
        if home_u > GF:
            scores_exacts = [ x for x in scores_exacts if x.home_score >= 1]
            
        if away_u > GF:
            scores_exacts = [ x for x in scores_exacts if x.away_score >= 1]

            
        calcul = {"p1_5": 0,  "m3_5": 0, "home": 0, "away": 0, "nul":0, "cs": 0, "btts": 0}
        for x in scores_exacts:
            if x.home_score > x.away_score:
                calcul["home"] += 1
            if x.home_score < x.away_score:
                calcul["away"] += 1
            if x.home_score == x.away_score:
                calcul["nul"] += 1
            if x.total() > 2.5:
                calcul["p1_5"] += 1
            if x.total() < 2.5:
                calcul["m3_5"] += 1
            if x.home_score > 0 and x.away_score > 0:
                calcul["btts"] += 1
            else:
                calcul["cs"] += 1          
        
        if calcul["nul"] == 0:
            scores_exacts = [ x for x in scores_exacts if x.home_score != x.away_score ] 
            scores_exacts = [ x for x in scores_exacts if x.home_score >= x.away_score  <= 2] 
        home_binomial = bimodal_poisson(home_stats.avg_goals_scored, away_stats.avg_goals_conceded)
        away_binomial = bimodal_poisson(away_stats.avg_goals_scored, home_stats.avg_goals_conceded)
        for x in scores_exacts:
            x.pct = round(home_binomial.get(x.home_score) * away_binomial.get(x.away_score), 2)

        
        for x in scores_exacts:
            if x.home_score > x.away_score:
                x.pct *= (1 + calcul["home"]/len(scores_exacts))
            if x.home_score < x.away_score:
                x.pct *= (1 + calcul["away"]/len(scores_exacts))
            if x.home_score == x.away_score:
                x.pct *= (1 + calcul["nul"]/len(scores_exacts))
            if x.total() > 1.5:
                x.pct *= (1 + calcul["p1_5"]/len(scores_exacts))
            if x.total() < 3.5:
                x.pct *= (1 + calcul["m3_5"]/len(scores_exacts))
            if x.home_score > 0 and x.away_score > 0:
                x.pct *= (1 + calcul["btts"]/len(scores_exacts))
            else:
                x.pct *= (1 + calcul["cs"]/len(scores_exacts))
                
            if (home.defense < 8 and away.defense < 7):
                if x.total() > 1.5:
                    x.pct *= 1.9
            if (home.dynamique >= 12  and  away.defense <= 5):
                if x.home_score > x.away_score:
                    x.pct *= 1.90
                    
            if (before_home.avg_goals_scored + before_away.avg_goals_conceded + before_home.avg_goals_conceded + before_away.avg_goals_scored) / 4 > GF:
                if x.total() > 1.5:
                    x.pct *= 1.9    
            if home_u > GF:
                if x.home_score > 0:
                    x.pct *= 1.90
                
            if away_u > GF:
                if x.away_score > 0:
                    x.pct *= 1.90

            if home.dynamique > away.dynamique and home.attack > away.attack:
                if x.home_score > x.away_score:
                    x.pct *= 1.6
                    
            if home.dynamique < away.dynamique and home.attack < away.attack:
                if x.total() <= 3:
                    x.pct *= 1.6

            if away.defense > home.defense:
                if abs(x.home_score - x.away_score) <= 2:
                    x.pct *= 1.4
                    
            if away.attack + home.attack > 15 and away.defense + home.defense > 26:
                if x.total() <= 3:
                    x.pct *= 1.4
                
        scores_exacts = sorted(scores_exacts, key=lambda x: -x.pct)[:6]
        # scores_exacts = [ x for x in scores_exacts if x.pct > 0.14]

        return scores_exacts
    
    except Exception as e:
        print(e)
