from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from annoying.decorators import render_to
from django.http import HttpResponseRedirect
from .models import *
from datetime import datetime
from coreApp.functions import *
from predictionApp.models import *
from competitionApp.models import *
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
        ratio = int(round((success.count() / predictions.count())*100, 2)) if predictions.count() > 0 else 0
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