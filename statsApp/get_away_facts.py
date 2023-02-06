import fixtureApp
from .models import *
from django.db.models import Avg, Sum, Q


def main(edit):
    for match in edit.edition_du_match.all():
        if match.match_facts.all().count() == 0 :
            function(match)
           

def function(match):
    
    MIN = 0.2
    MAX = 0.8
    MIN_GOAL = 1
    MAX_GOAL = 2
    #Home
    edition = match.edition

    matchs_away = fixtureApp.models.Match.objects.filter(edition = edition, is_finished=True, date__gte = edition.start_date, date__lt = match.date , away = match.away).order_by('-date')
    matchs_away_all = match.away.get_last_matchs(match, 100, edition = True)
    
    
    #toute victoire de l'equipe qui joue à l'extérieur
    if len(matchs_away_all) >= 7:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away_all):
            total = 0
            for x in matchs_away_all[0:i]:
                result = x.get_result()
                total += 1 if ((result.home_score > result.away_score and x.home == match.away) or (result.home_score < result.away_score and x.away == match.away)) else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "Win"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "Win"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
                
                
                


    # #defaite de l'equipe qui joue à l'extérieur
    if len(matchs_away_all) >= 7:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away_all):
            total = 0
            for x in matchs_away_all[0:i]:
                result = x.get_result()
                total += 1 if ((result.home_score < result.away_score and x.home == match.away) or (result.home_score > result.away_score and x.away == match.away)) else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "Lose"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "Lose"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )




    # nul de l'equipe qui joue à l'extérieur
    if len(matchs_away_all) >= 7:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away_all):
            total = 0
            for x in matchs_away_all[0:i]:
                result = x.get_result()
                total += 1 if (result.home_score == result.away_score ) else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "Draw"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "Draw"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
    
    
    
    # btts de l'equipe qui joue à l'extérieur
    if len(matchs_away_all) >= 7:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away_all):
            total = 0
            for x in matchs_away_all[0:i]:
                result = x.get_result()
                total += 1 if (result.home_score > 0 and result.away_score > 0 ) else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "btts"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "btts"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
    
    
    
    # clean sheet de l'equipe qui joue à l'extérieur
    if len(matchs_away_all) >= 7:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away_all):
            total = 0
            for x in matchs_away_all[0:i]:
                result = x.get_result()
                total += 1 if ((result.away_score == 0 and x.home == match.away) or (result.home_score == 0 and x.away == match.away)) else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "CS"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "CS"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
    
    
    
    # au moins un but concédé pour l'equipe qui joue à l'extérieur
    if len(matchs_away_all) >= 7:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away_all):
            total = 0
            for x in matchs_away_all[0:i]:
                result = x.get_result()
                total += 1 if ((result.away_score > 0 and x.home == match.away) or (result.home_score > 0 and x.away == match.away)) else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "GC"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "GC"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
    
    
    # au moins un but marqué pour l'equipe qui joue à l'extérieur
    if len(matchs_away_all) >= 7:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away_all):
            total = 0
            for x in matchs_away_all[0:i]:
                result = x.get_result()
                total += 1 if ((result.home_score > 0 and x.home == match.away) or (result.away_score > 0 and x.away == match.away)) else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "GS"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "GS"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
    
    
    
    
    # au moins deux but dans le match
    if len(matchs_away_all) >= 7:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away_all):
            total = 0
            for x in matchs_away_all[0:i]:
                result = x.get_result()
                total += 1 if result.home_score + result.away_score > 1.5 else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "p1_5"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "p1_5"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
    
    
    
    
    # au plus trois but dans le match
    if len(matchs_away_all) >= 7:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away_all):
            total = 0
            for x in matchs_away_all[0:i]:
                result = x.get_result()
                total += 1 if result.home_score + result.away_score < 3.5 else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "m3_5"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "m3_5"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
    
    
    
    
    # moyenne but marqué dans le match
    if len(matchs_away_all) >= 7:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away_all):
            total = 0
            for x in matchs_away_all[0:i]:
                result = x.get_result()
                total += result.home_score if x.home == match.away else result.away_score
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN_GOAL and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "TGS"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX_GOAL and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "TGS"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
    
    
    
    
    # total but concédé dans le match
    if len(matchs_away_all) >= 7:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away_all):
            total = 0
            for x in matchs_away_all[0:i]:
                result = x.get_result()
                total += result.away_score if x.home == match.away else result.home_score
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN_GOAL and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "TGC"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX_GOAL and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "TGC"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
    
    ########################################################################################################################################################################################
    ########################################################################################################################################################################################
    ########################################################################################################################################################################################
    
    
    
    
    #victoire à l'extérieur de l'equipe qui joue à l'extérieur
    if len(matchs_away) >= 4:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away):
            total = 0
            for x in matchs_away[0:i]:
                result = x.get_result()
                if result.home_score < result.away_score:
                    total += 1
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "Win"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "Win"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
    
    
    
    # #defaite à l'extérieur de l'equipe qui joue à l'extérieur
    if len(matchs_away) >= 4:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away):
            total = 0
            for x in matchs_away[0:i]:
                result = x.get_result()
                total += 1 if result.home_score > result.away_score  else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "Lose"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "Lose"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
       
        
    # #nul à l'extérieur de l'equipe qui joue à l'extérieur
    if len(matchs_away) >= 4:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away):
            total = 0
            for x in matchs_away[0:i]:
                result = x.get_result()
                total += 1 if (result.home_score == result.away_score) else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "Draw"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "Draw"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
       
        
    # #btts à l'extérieur de l'equipe qui joue à l'extérieur
    if len(matchs_away) >= 4:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away):
            total = 0
            for x in matchs_away[0:i]:
                result = x.get_result()
                total += 1 if (result.home_score > 0 and result.away_score > 0 ) else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "btts"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "btts"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
       
        
    # #clean sheet à l'extérieur de l'equipe qui joue à l'extérieur
    if len(matchs_away) >= 4:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away):
            total = 0
            for x in matchs_away[0:i]:
                result = x.get_result()
                total += 1 if result.home_score == 0 else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "CS"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "CS"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
       
        
    # #au moins un but concedé à l'extérieur pour l'equipe qui joue à l'extérieur
    if len(matchs_away) >= 4:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away):
            total = 0
            for x in matchs_away[0:i]:
                result = x.get_result()
                total += 1 if result.home_score > 0 else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "GC"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "GC"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
                
    
       
        
    # #au moins un but marqué à l'extérieur pour l'equipe qui joue à l'extérieur
    if len(matchs_away) >= 4:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away):
            total = 0
            for x in matchs_away[0:i]:
                result = x.get_result()
                total += 1 if result.away_score > 0 else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "GS"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "GS"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
       
        
    # #au moins deux but marqué à l'extérieur pour l'equipe qui joue à l'extérieur
    if len(matchs_away) >= 4:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away):
            total = 0
            for x in matchs_away[0:i]:
                result = x.get_result()
                total += 1 if result.home_score + result.away_score > 1.5 else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "p1_5"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "p1_5"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
       
        
    # #au plus trois but marqué à l'extérieur pour l'equipe qui joue à l'extérieur
    if len(matchs_away) >= 4:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away):
            total = 0
            for x in matchs_away[0:i]:
                result = x.get_result()
                total += 1 if result.home_score + result.away_score < 3.5 else 0
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "m3_5"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "m3_5"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
       
        
    #moyenne but marqué à l'extérieur pour l'equipe qui joue à l'extérieur
    if len(matchs_away) >= 4:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away):
            total = 0
            for x in matchs_away[0:i]:
                result = x.get_result()
                total += result.away_score
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN_GOAL and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "TGS"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX_GOAL and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "TGS"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
    
       
        
    # moyenne but concédé à l'extérieur pour l'equipe qui joue à l'extérieur
    if len(matchs_away) >= 4:
        i = 7
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs_away):
            total = 0
            for x in matchs_away[0:i]:
                result = x.get_result()
                total += result.home_score
            if total / i >= taux_max:
                taux_max = total / i
                tableau_max = {}
                tableau_max[i] = total
            if total / i <= taux_min:
                taux_min = total / i
                tableau_min = {}
                tableau_min[i] = total
            i += 1
        
        if taux_min <= MIN_GOAL and len (tableau_min) > 0:
            for k, v in tableau_min.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "TGC"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
        
        elif taux_max >= MAX_GOAL and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                Fact.objects.get_or_create(
                    type = TypeFact.objects.get(name = "TGC"),
                    full_time = True,
                    all_matches = False,
                    match = match,
                    team = match.away,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )