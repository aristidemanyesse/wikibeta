from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from annoying.decorators import render_to
from django.http import HttpResponseRedirect
from .models import *
from datetime import datetime, timedelta
from dateutils import relativedelta
from coreApp.functions import *
from predictionApp.models import *
from competitionApp.models import *
from bettingApp.models import *
import statsApp.get_recherche_facts as get_recherche_facts
import math
# Create your views here.


@render_to('statsApp/index.html')
def statistiques(request):
    if request.method == "GET":
        datas = Prediction.objects.filter(is_checked = None)
        for predict in datas:
            predict.validity()
              
        modes = {}
        for mode in ModePrediction.objects.all():
            total = Prediction.objects.filter(mode = mode).exclude(is_checked = None)
            modes[mode] = round((total.filter(is_checked = True).count() / total.count()) *100, 2) if total.count() > 0 else 0
           
        types = {}
        for type in TypePrediction.objects.all():
            total = Prediction.objects.filter(type = type).exclude(is_checked = None)
            types[type] = round((total.filter(is_checked = True).count() / total.count()) *100, 2) if total.count() > 0 else 0
            
        
        tableau = {}
        for mode in ModePrediction.objects.all():
            for type in TypePrediction.objects.all():
                total = Prediction.objects.filter(type = type, mode = mode).exclude(is_checked = None)
                tableau[mode, type] = round((total.filter(is_checked = True).count() / total.count()) *100, 2) if total.count() > 0 else 0
            
            
        predictions = Prediction.objects.exclude(is_checked = None)
        success = predictions.filter(is_checked = True)
        ratio = int((success.count() / predictions.count()) * 100)
        decimal = int(((success.count() / predictions.count() * 100) - ratio) * 100)
        
        
        now = datetime.now() - timedelta()
        i = 24
        stats_pre = {}
        stats_total = {}
        stats_pct = {}
        while i > 0:
            fin  = now
            now = now - relativedelta(months=1)
            predicts = Prediction.objects.filter(match__date__gte = now, match__date__lt = fin)
            total = 0
            for x in predicts:
                total += 1 if x.is_checked else 0
                
            stats_pre[now] = predicts.count()
            stats_total[now] = total
            stats_pct[now] = round(total / predicts.count() * 100)
            
            i-=1
        
        ctx = {
            "modes" : modes,
            "types" : types,
            "predictions" : predictions,
            "tableau" : tableau,
            "ratio" : ratio,
            "decimal" : decimal,
            "stats_pre" : stats_pre,
            "stats_pct" : stats_pct,
            "stats_total" : stats_total,
        }
        return ctx
    
    




@render_to('statsApp/rechercher_cote.html')
def rechercher_cote(request, home, away, draw):
    if request.method == "GET":
        date = datetime.now()
        home = float(home)
        draw = float(draw)
        away = float(away)
        
        similaires_matchs = []
        odds = OddsMatch.objects.filter(match__is_finished = True, home__range = intervale(home), away__range = intervale(away), draw__range = intervale(draw), match__date__year__gte = date.year-1).order_by("-match__date")
        for odd in odds:
            if odd.match not in similaires_matchs:
                similaires_matchs.append(odd.match)
               
        
        facts = get_recherche_facts.function(similaires_matchs) if len(similaires_matchs) > 0 else []
        ctx = {
               "home": home,
               "away": away,
               "draw": draw,
               "similaires_matchs": similaires_matchs[:30],
               "facts": facts,
            }
        return ctx
    
    




@render_to('statsApp/rechercher_ppg.html')
def rechercher_ppg(request, home, away):
    if request.method == "GET":
        date = datetime.now()
        home = float(home)
        away = float(away)
        
        similaires_matchs = []
        befores = BeforeMatchStat.objects.filter(match__is_finished = True, ppg__range = intervale(home), match__date__year__gte = date.year-1).order_by("-match__date")
        for bef in befores:
            befs = BeforeMatchStat.objects.filter(ppg__range = intervale(away), match = bef.match).exclude(id = bef.id)
            if len(befs) == 1:
                similaires_matchs.append(bef.match)
               
        facts = get_recherche_facts.function(similaires_matchs) if len(similaires_matchs) > 0 else []
        ctx = {
               "home": home,
               "away": away,
               "similaires_matchs": similaires_matchs[:30],
               "facts": facts,
            }
        return ctx