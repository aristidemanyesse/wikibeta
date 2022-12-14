from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from annoying.decorators import render_to
from django.http import HttpResponseRedirect
from .models import *
from datetime import datetime, timedelta
from coreApp.functions import *
from predictionApp.models import *
from competitionApp.models import *
# Create your views here.


@render_to('fixtureApp/index.html')
def home(request):
    if request.method == "GET":
        date = datetime.now()
        return HttpResponseRedirect(reverse('fixtureApp:fixtures', args=[date.year, date.month, date.day]))
        

@render_to('fixtureApp/index.html')
def fixtures(request, year, month, day):
    if request.method == "GET":
        datas = Prediction.objects.filter(is_checked = None)
        for predict in datas:
            predict.validity()
            
        date = datetime(year, month, day)
        datas = {}
        for edition in EditionCompetition.objects.filter(is_finished=False):
            matchs = Match.objects.filter(date = date, edition = edition)
            if len(matchs) > 0 :
                datas[edition] = matchs
                
        ctx = {
            "av_hier"     : date - timedelta(days=2),
            "hier"        : date - timedelta(days=1),
            "date"        : date,
            "demain"      : date + timedelta(days=1),
            "ap_demain"   : date + timedelta(days=2),
            "datas"       : datas,
        }
        return ctx
        
        

@render_to('fixtureApp/match.html')
def match(request, id):
    if request.method == "GET":
        match = Match.objects.get(id=id)
        confrontations = match.confrontations_directes()
        predictions = match.prediction_match.filter()
        
        home_last_matchs = match.home.get_last_matchs(match, number = 10, edition = True)
        home_last_forms = match.home.get_last_form(match, number = 5, edition = True)
        away_last_matchs = match.away.get_last_matchs(match, number = 10, edition = True)
        away_last_forms = match.away.get_last_form(match, number = 5, edition = True)
        
        home_facts = match.match_facts.filter(team = match.home)
        away_facts = match.match_facts.filter(team = match.away)

        ctx = {
            "match" : match,
            "confrontations" : confrontations[:10],
            "predictions" : predictions,
            "home_last_matchs" : home_last_matchs,
            "home_last_forms" : home_last_forms,
            "away_last_matchs" : away_last_matchs,
            "away_last_forms" : away_last_forms,
            "home_facts" : home_facts,
            "away_facts" : away_facts,
        }
        return ctx
