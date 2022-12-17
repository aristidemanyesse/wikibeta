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


@render_to('fixtureApp/index.html')
def home(request):
    if request.method == "GET":
        matchs = Match.objects.filter(is_finished=False)
        ctx = {
            "matchs" : matchs
        }
        return ctx
        

@render_to('fixtureApp/index.html')
def fixtures(request, year, month, day):
    if request.method == "GET":
        date = datetime(year, month, day)
        datas = {}
        for edition in EditionCompetition.objects.filter(is_finished=False):
            matchs = Match.objects.filter(date = date, edition = edition).order_by("-date")
            if len(matchs) > 0 :
                datas[edition] = matchs
                
        ctx = {
            "date" : date,
            "datas" : datas,
        }
        return ctx
        
        

@render_to('fixtureApp/match.html')
def match(request, id):
    if request.method == "GET":
        confrontations = match.confrontations_directes()
        predictions = match.prediction_match.filter()

        ctx = {
            "confrontations" : confrontations[:10],
            "predictions" : predictions,
        }
        return ctx
