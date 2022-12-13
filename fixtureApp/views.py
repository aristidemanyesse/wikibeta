from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
import datetime
from django.http import HttpResponseRedirect
from .models import *
from coreApp.functions import *
from predictionApp.models import *
# Create your views here.



def home(request):
    if request.method == "GET":
        ctx = {}
        return render(request, "features/index.html", ctx)
        
        




    
def match(request, id):
    if request.method == "GET":
        match = Match.objects.get( id = id)
        confrontations = match.confrontations_directes()
        predictions = match.prediction_match.filter()
        
        datas = match.get_home_recents_matchs(edition = True)
        buts = total = 0
        if len(datas) > 4:
            for x in datas:
                if x.home == match.home:
                    buts += x.home_score
                    total += 1
        moyp = buts / total
        
        print(moyp)
        for x in [0.5, 1.5, 2.5, 3.5]:
            print(x, "+++++++++++>", fish_law_plus(moyp, x))

            
            
        print("---------------------------------------------------------")
        
        datas = match.get_away_recents_matchs(edition = True)
        gc = total=  0
        if len(datas) > 4:
            for x in datas:
                if x.away == match.away:
                    gc += x.home_score
                    total += 1
        moym = gc / total
        
        print(moym)
        for x in [0.5, 1.5, 2.5, 3.5]:
            print(x, "======>", fish_law_plus(moym, x))

        # moy = moyenne_harmonique(moyp, moym)
        
        # print(len(datas), moyp, moym,  moy)
        # print(moyp)
        # for x in [0.5, 1.5, 2.5, 3.5]:
        #     print(x, "+++++++++++>", fish_law_plus(moyp, x))
        ctx = {
            "match" : match,
            "confrontations" : confrontations[:10],
            "predictions" : predictions,
            }
        return render(request, "features/match.html", ctx)
