from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from annoying.decorators import render_to
from django.http import HttpResponseRedirect
from .models import *
from datetime import datetime
from coreApp.functions import *
from predictionApp.models import *
from competitionApp.models import *
from bettingApp.models import *
import statsApp.get_recherche_facts as get_recherche_facts

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
        ratio = round((success.count() / predictions.count())*100, 2) if predictions.count() > 0 else 0
        
        matchs = Match.objects.filter(is_finished=False)
        ctx = {
            "modes" : modes,
            "types" : types,
            "predictions" : predictions,
            "tableau" : tableau,
            "ratio" : ratio,
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
               
        
        facts = get_recherche_facts.function(similaires_matchs[:100])
        ctx = {
               "home": home,
               "away": away,
               "draw": draw,
               "similaires_matchs": similaires_matchs[:30],
               "facts": facts,
            }
        return ctx
    
    




@render_to('statsApp/rechercher_ppg.html')
def rechercher_ppg(request):
    if request.method == "GET":
        
        
            
        ctx = {
               
            }
        return ctx