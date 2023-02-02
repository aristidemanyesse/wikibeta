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

def intersection(list1, list2):
    return [value for value in list1 if value in list2]


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
        predictions = match.prediction_match.filter()
        
        home_last_matchs = match.home.get_last_matchs(match, number = 10, edition = True)
        home_last_forms = match.home.get_last_form(match, number = 5, edition = True)
        away_last_matchs = match.away.get_last_matchs(match, number = 10, edition = True)
        away_last_forms = match.away.get_last_form(match, number = 5, edition = True)
        
        home_facts = match.match_facts.filter(team = match.home)
        away_facts = match.match_facts.filter(team = match.away)
        
        extra_infos = match.get_extra_info_match()
        
        stats = match.get_home_before_stats()
        confrontations = Match.objects.filter(id__in = eval(stats.list_confrontations)).order_by("-date")
        similaires_ppg = Match.objects.filter(id__in = eval(stats.list_similaires_ppg)).order_by("-date")
        similaires_ppg2 = Match.objects.filter(id__in = eval(stats.list_similaires_ppg2)).order_by("-date")
        similaires_betting = Match.objects.filter(id__in = eval(stats.list_similaires_betting)).order_by("-date")
        inter = intersection(similaires_ppg, similaires_betting)
        
        
        home_rank = LigneRanking.objects.filter(team = match.home, created_at__lte = match.date).order_by('-created_at').first()
        away_rank = LigneRanking.objects.filter(team = match.away, created_at__lte = match.date).order_by('-created_at').first()
                
        rank = match.edition.edition_rankings.filter(created_at__lte = match.date).order_by('-created_at').first()
        
        competitionstats = match.edition.edition_stats.filter(created_at__lte = match.date).order_by('-created_at').first()

        ctx = {
            "match" : match,
            "confrontations" : confrontations[:10],
            "similaires_ppg" : similaires_ppg,
            "similaires_ppg2" : similaires_ppg2,
            "similaires_betting" : similaires_betting,
            "inter" : inter,
            "predictions" : predictions,
            "home_last_matchs" : home_last_matchs,
            "home_last_forms" : home_last_forms,
            "away_last_matchs" : away_last_matchs,
            "away_last_forms" : away_last_forms,
            "home_facts" : home_facts,
            "away_facts" : away_facts,
            "extra_infos" : extra_infos,
            "rank" : rank,
            "home_rank" : home_rank,
            "away_rank" : away_rank,
            "competitionstats" : competitionstats,
        }
        return ctx
