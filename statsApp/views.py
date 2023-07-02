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


@render_to('statsApp/test.html')
def test(request):
    data1 = []
    data2 = []
    for match in Match.objects.filter(is_finished = True).exclude(is_posted = True).order_by('-date')[:1000]:
        extra = match.get_extra_info_match()
        home_stats = match.get_home_before_stats()
        away_stats = match.get_away_before_stats()
        if extra is not None and home_stats is not None and away_stats is not None: 
            pre = ((home_stats.avg_corners_for or 0) + (home_stats.avg_corners_against or 0) + (away_stats.avg_corners_for or 0) + (away_stats.avg_corners_against or 0)) / 2
            out = (extra.home_corners or 0 )+ (extra.away_corners or 0)
            if not pre == out == 0:
                data1.append(round(pre))
                data2.append(round(out))
        
        
    ctx = {
        "data1" : data1,
        "data2" : data2,
        }
    return ctx



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
        count = predictions.count()
        ratio = int((success.count() / count) * 100) if count > 0 else 0
        decimal = int(((success.count() / count * 100) - ratio) * 100) if count > 0 else 0
        
        
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
            stats_pct[now] = round(total / predicts.count() * 100) if predicts.count() > 0 else 0
            
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
    


@render_to('statsApp/indextest.html')
def statistiquestest(request):
    if request.method == "GET":
        datas = PredictionTest.objects.filter(is_checked = None)
        for predict in datas:
            predict.validity()
              
        modes = {}
        for mode in ModePrediction.objects.all():
            total = PredictionTest.objects.filter(mode = mode).exclude(is_checked = None)
            modes[mode] = round((total.filter(is_checked = True).count() / total.count()) *100, 2) if total.count() > 0 else 0
           
        types = {}
        tableau_nb = {}
        for type in TypePrediction.objects.all():
            total = PredictionTest.objects.filter(type = type).exclude(is_checked = None)
            types[type] = round((total.filter(is_checked = True).count() / total.count()) *100, 2) if total.count() > 0 else 0
            tableau_nb[type] = total.filter().count()
            
        
        tableau = {}
        for mode in ModePrediction.objects.all():
            for type in TypePrediction.objects.all():
                total = PredictionTest.objects.filter(type = type, mode = mode).exclude(is_checked = None)
                tableau[mode, type] = round((total.filter(is_checked = True).count() / total.count()) *100, 2) if total.count() > 0 else 0
            
            
        predictions = PredictionTest.objects.exclude(is_checked = None)
        success = predictions.filter(is_checked = True)
        count = predictions.count()
        ratio = int((success.count() / count) * 100) if count > 0 else 0
        decimal = int(((success.count() / count * 100) - ratio) * 100) if count > 0 else 0
        
        
        now = datetime.now() - timedelta()
        i = 24
        stats_pre = {}
        stats_total = {}
        stats_pct = {}
        while i > 0:
            fin  = now
            now = now - relativedelta(months=1)
            predicts = PredictionTest.objects.filter(match__date__gte = now, match__date__lt = fin)
            total = 0
            for x in predicts:
                total += 1 if x.is_checked else 0
                
            stats_pre[now] = predicts.count()
            stats_total[now] = total
            stats_pct[now] = round(total / predicts.count() * 100) if predicts.count() > 0 else 0
            
            i-=1
        
        ctx = {
            "modes" : modes,
            "types" : types,
            "predictions" : predictions,
            "tableau" : tableau,
            "tableau_nb" : tableau_nb,
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
        date = datetime.now() - timedelta(days =5 * 12 * 30)
        home = float(home)
        draw = float(draw)
        away = float(away)
        
        similaires_matchs = []
        odds = OddsMatch.objects.filter(match__is_finished = True, home__range = intervale(home), away__range = intervale(away), draw__range = intervale(draw), match__date__gte = date).order_by("-match__date")
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
        date = datetime.now() - timedelta(days = 12 * 30)
        home = float(home)
        away = float(away)
        
        similaires_matchs = []
        befores = BeforeMatchStat.objects.filter(match__is_finished = True, ppg__range = intervale(home), match__date__gte = date).order_by("-match__date")
        for bef in befores:
            if bef.team == bef.match.home:
                befs = BeforeMatchStat.objects.filter(ppg__range = intervale(away), match = bef.match).exclude(id = bef.id)
                if len(befs) == 1:
                    similaires_matchs.append(bef.match)
               
        facts = get_recherche_facts.function(similaires_matchs[:100]) if len(similaires_matchs) > 0 else []
        ctx = {
               "home": home,
               "away": away,
               "total": len(similaires_matchs),
               "similaires_matchs": similaires_matchs[:20],
               "facts": facts,
            }
        return ctx