from django.core.management.base import BaseCommand, CommandError
from predictionApp.models import *
from competitionApp.models import *
from fixtureApp.models import *
from dateparser import parse



def before_stats(edit:EditionCompetition): 
    for match in edit.edition_du_match.filter().order_by("-date"):
        for team in [match.home, match.away]:
            points = 0
            scored = 0
            conceded = 0
            
            befores = Match.objects.filter(date__lt = match.date, edition = match.edition).filter(Q(home=team) | Q(away=team)).order_by("date")
            for m in befores:
                points += m.points_for_this_macth(match.home if (match.home == team) else match.away)
                scored += m.goals_scored(match.home if (match.home == team) else match.away)
                conceded += m.goals_conceded(match.home if (match.home == team) else match.away)
            
            bef, created = BeforeMatchStat.objects.get_or_create(
                match = match,
                team = match.home if (match.home == team) else match.away,
                ppg = round((points / len(befores)), 2) if len(befores) > 0 else 0,
                goals_scored = scored,
                avg_goals_scored = round((scored / len(befores)), 2) if len(befores) > 0 else 0,
                goals_conceded = conceded,
                avg_goals_conceded = round((conceded / len(befores)), 2) if len(befores) > 0 else 0
            )
        
            print(bef, created)

    
    
    

def p1(edit):
    for match in edit.edition_du_match.filter().order_by("-date"):
        print("Prédiction pour {}".format(match))
        matchs = match.confrontations_directes()
        if len(matchs) >= 14 :
            moy = 0
            for x in matchs:
                moy += (x.home_score + x.away_score) / len(matchs)
                
                
            if (moy >= 2.7):
                for x in [1.5, 2.5, 3.5]:
                    p = fish_law_plus(moy, x)
                    if p >= 85:
                        Prediction.objects.create(
                            mode = ModePrediction.get("M1"),
                            type = TypePrediction.get("p{}".format(str(x).replace(".", "_"))),
                            match = match,
                            pct = p
                        )
                    
                    
            if (moy <= 2):
                for x in [2.5, 3.5]:
                    p = fish_law_moins(moy, x)
                    if p >= 85:
                        Prediction.objects.create(
                            mode = ModePrediction.get("M1"),
                            type = TypePrediction.get("m{}".format(str(x).replace(".", "_"))),
                            match = match,
                            pct = p
                        )
                        
                        




def p2(edit):
    for match in edit.edition_du_match.filter().order_by("-date"):
        print("Prédiction pour {}".format(match))
        matchs = match.similaires_ppg()
        if len(matchs) >= 14 :
            moy = 0
            for x in matchs:
                moy += (x.home_score + x.away_score) / len(matchs)
                
            if (moy >= 2.7):
                for x in [1.5, 2.5, 3.5]:
                    p = fish_law_plus(moy, x)
                    if p >= 85:
                        Prediction.objects.create(
                            mode = ModePrediction.get("M2"),
                            type = TypePrediction.get("p{}".format(str(x).replace(".", "_"))),
                            match = match,
                            pct = p
                        )
                    
                    
            if (moy <= 2):
                for x in [1.5, 2.5, 3.5]:
                    p = fish_law_moins(moy, x)
                    if p >= 85:
                        Prediction.objects.create(
                            mode = ModePrediction.get("M2"),
                            type = TypePrediction.get("m{}".format(str(x).replace(".", "_"))),
                            match = match,
                            pct = p
                        )
                        
                        
                        

def p4(edit):
    for match in edit.edition_du_match.filter().order_by("-date"):
        print("Prédiction pour {}".format(match))
        matchs = match.similaires_betting()
        if len(matchs) >= 21 :
            moy = 0
            for x in matchs:
                moy += (x.home_score + x.away_score) / len(matchs)
            
            if (moy >= 2.7):
                for x in [1.5, 2.5, 3.5]:
                    p = fish_law_plus(moy, x)
                    if p >= 85:
                        Prediction.objects.create(
                            mode = ModePrediction.get("M4"),
                            type = TypePrediction.get("p{}".format(str(x).replace(".", "_"))),
                            match = match,
                            pct = p
                        )
                    
                    
            if (moy <= 2):
                for x in [1.5, 2.5, 3.5]:
                    p = fish_law_moins(moy, x)
                    if p >= 85:
                        Prediction.objects.create(
                            mode = ModePrediction.get("M4"),
                            type = TypePrediction.get("m{}".format(str(x).replace(".", "_"))),
                            match = match,
                            pct = p
                        )