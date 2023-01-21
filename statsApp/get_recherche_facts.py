import fixtureApp
from .models import *
from django.db.models import Avg, Sum, Q


def function(matchs):
    
    MIN = 0.25
    MAX = 0.75
    MIN_GOAL = 1.7
    MAX_GOAL = 2.7
    
    match = matchs[0]
    facts = []

    
    #victoire à domicile de l'equipe qui joue à domicile
    if len(matchs) >= 10:
        i = round(len(matchs) / 2)
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs):
            total = 0
            for x in matchs[0:i]:
                result = x.get_result()
                if result.home_score > result.away_score:
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
                fact = Fact(
                    type = TypeFact.objects.get(name = "Win"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
                facts.append(fact)
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                fact = Fact(
                    type = TypeFact.objects.get(name = "Win"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
                facts.append(fact)
    
    
    
    
    # #defaite à domicile de l'equipe qui joue à domicile
    if len(matchs) >= 10:
        i = round(len(matchs) / 2)
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs):
            total = 0
            for x in matchs[0:i]:
                result = x.get_result()
                total += 1 if result.home_score < result.away_score  else 0
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
                fact = Fact(
                    type = TypeFact.objects.get(name = "Lose"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
                facts.append(fact)
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                fact = Fact(
                    type = TypeFact.objects.get(name = "Lose"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
                facts.append(fact)
       
        
    # #nul à domicile de l'equipe qui joue à domicile
    if len(matchs) >= 10:
        i = round(len(matchs) / 2)
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs):
            total = 0
            for x in matchs[0:i]:
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
                fact = Fact(
                    type = TypeFact.objects.get(name = "Draw"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
                facts.append(fact)
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                fact = Fact(
                    type = TypeFact.objects.get(name = "Draw"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
                facts.append(fact)
    
       
        
    # #btts à domicile de l'equipe qui joue à domicile
    if len(matchs) >= 10:
        i = round(len(matchs) / 2)
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs):
            total = 0
            for x in matchs[0:i]:
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
                fact = Fact(
                    type = TypeFact.objects.get(name = "btts"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
                facts.append(fact)
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                fact = Fact(
                    type = TypeFact.objects.get(name = "btts"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
                facts.append(fact)
    
       
        
    # #clean sheet à domicile de l'equipe qui joue à domicile
    if len(matchs) >= 10:
        i = round(len(matchs) / 2)
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs):
            total = 0
            for x in matchs[0:i]:
                result = x.get_result()
                total += 1 if result.away_score == 0 else 0
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
                fact = Fact(
                    type = TypeFact.objects.get(name = "CS"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
                facts.append(fact)
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                fact = Fact(
                    type = TypeFact.objects.get(name = "CS"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
                facts.append(fact)
    
       
        
    # #au moins un but concedé à domicile pour l'equipe qui joue à domicile
    if len(matchs) >= 10:
        i = round(len(matchs) / 2)
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs):
            total = 0
            for x in matchs[0:i]:
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
                fact = Fact(
                    type = TypeFact.objects.get(name = "GC"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
                facts.append(fact)
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                fact = Fact(
                    type = TypeFact.objects.get(name = "GC"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
                facts.append(fact)
                
    
       
        
    # #au moins un but marqué à domicile pour l'equipe qui joue à domicile
    if len(matchs) >= 10:
        i = round(len(matchs) / 2)
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs):
            total = 0
            for x in matchs[0:i]:
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
                fact = Fact(
                    type = TypeFact.objects.get(name = "GS"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
                facts.append(fact)
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                fact = Fact(
                    type = TypeFact.objects.get(name = "GS"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
                facts.append(fact)
       
        
    # #au moins deux but marqué à domicile pour l'equipe qui joue à domicile
    if len(matchs) >= 10:
        i = round(len(matchs) / 2)
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs):
            total = 0
            for x in matchs[0:i]:
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
                fact = Fact(
                    type = TypeFact.objects.get(name = "p1_5"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
                facts.append(fact)
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                fact = Fact(
                    type = TypeFact.objects.get(name = "p1_5"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
                facts.append(fact)
    
       
        
    # #au plus trois but marqué à domicile pour l'equipe qui joue à domicile
    if len(matchs) >= 10:
        i = round(len(matchs) / 2)
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs):
            total = 0
            for x in matchs[0:i]:
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
                fact = Fact(
                    type = TypeFact.objects.get(name = "m3_5"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
                facts.append(fact)
        
        elif taux_max >= MAX and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                fact = Fact(
                    type = TypeFact.objects.get(name = "m3_5"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
                facts.append(fact)
    
       
        
    #moyenne but marqué à domicile pour l'equipe qui joue à domicile
    if len(matchs) >= 10:
        i = round(len(matchs) / 2)
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs):
            total = 0
            for x in matchs[0:i]:
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
                fact = Fact(
                    type = TypeFact.objects.get(name = "TGS"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
                facts.append(fact)
        
        elif taux_max >= MAX_GOAL and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                fact = Fact(
                    type = TypeFact.objects.get(name = "TGS"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
                facts.append(fact)
    
       
        
    # moyenne but concédé à domicile pour l'equipe qui joue à domicile
    if len(matchs) >= 10:
        i = round(len(matchs) / 2)
        taux_min = 100
        tableau_min = {}
        taux_max = 0
        tableau_max = {}
        while i <= len(matchs):
            total = 0
            for x in matchs[0:i]:
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
                fact = Fact(
                    type = TypeFact.objects.get(name = "TGC"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_min, 2)
                )
                facts.append(fact)
        
        elif taux_max >= MAX_GOAL and len (tableau_max) > 0:
            for k, v in tableau_max.items():
                fact = Fact(
                    type = TypeFact.objects.get(name = "TGC"),
                    full_time = True,
                    all_matches = True,
                    match = match,
                    total = k,
                    success = v,
                    pct = round(taux_max, 2)
                )
                facts.append(fact)
                
    return facts