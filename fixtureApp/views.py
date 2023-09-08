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
            
        date = datetime(year, month, day).date()
        datas = {}
        for edition in EditionCompetition.objects.filter(start_date__lte = date, finish_date__gte = date):
            matchs = Match.objects.filter(date = date, edition = edition)
            if len(matchs) > 0 :
                datas[edition] = matchs
        
        today = datetime.now().date()
        ctx = {
            "av_hier"     : today - timedelta(days=2),
            "hier"        : today - timedelta(days=1),
            "date"        : date,
            "today"        : today,
            "demain"      : today + timedelta(days=1),
            "ap_demain"   : today + timedelta(days=2),
            "datas"       : datas,
        }
        return ctx
        
        

@render_to('fixtureApp/match.html')
def match(request, id):
    if request.method == "GET":
        match = Match.objects.get(id=id)
        predictions = match.prediction_match.filter()
        scores = match.predictionscore_match.filter()
        
        home_last_matchs = match.home.get_last_matchs(match, number = 10, edition = True)
        home_last_forms = match.home.get_last_form(match, number = 5, edition = True)
        
        away_last_matchs = match.away.get_last_matchs(match, number = 10, edition = True)
        away_last_forms = match.away.get_last_form(match, number = 5, edition = True)
        
        home_facts = match.match_facts.filter(team = match.home)
        away_facts = match.match_facts.filter(team = match.away)
        
        stats_home = match.get_home_before_stats()
        stats_away = match.get_away_before_stats()
        
        confrontations        = Match.objects.filter(id__in = eval(stats_home.list_confrontations)).order_by("-date")
        similaires_ppg        = Match.objects.filter(id__in = eval(stats_home.list_similaires_ppg)).order_by("-date")
        similaires_ppg2       = Match.objects.filter(id__in = eval(stats_home.list_similaires_ppg2)).order_by("-date")
        similaires_betting    = Match.objects.filter(id__in = eval(stats_home.list_similaires_betting)).order_by("-date")
        list_intercepts       = Match.objects.filter(id__in = eval(stats_home.list_intercepts)).order_by("-date")
        
        home_rank = LigneRanking.objects.filter(team = match.home, ranking__date__lte = match.date).order_by('-ranking__date').first()
        away_rank = LigneRanking.objects.filter(team = match.away, ranking__date__lte = match.date).order_by('-ranking__date').first()
        
        home_profile = match.match_profile.filter(team = match.home).order_by('-date').first()
        away_profile = match.match_profile.filter(team = match.away).order_by('-date').first()
                
        rank = match.edition.edition_rankings.filter(date__lte = match.date).order_by('-date').first()
        competitionstats = match.edition.edition_stats.filter(ranking__date__lte = match.date).order_by('-created_at').first()
        extra_infos = match.get_extra_info_match()

        ctx = {
            "match"                 : match,
            "confrontations"        : confrontations[:10],
            "similaires_ppg"        : similaires_ppg,
            "similaires_ppg2"       : similaires_ppg2,
            "similaires_betting"    : similaires_betting,
            "list_intercepts"       : list_intercepts,
            "predictions"           : predictions,
            "scores"                : scores,
            "home_last_matchs"      : home_last_matchs,
            "home_last_forms"       : home_last_forms,
            "away_last_matchs"      : away_last_matchs,
            "away_last_forms"       : away_last_forms,
            "home_facts"            : home_facts,
            "away_facts"            : away_facts,
            "extra_infos"           : extra_infos,
            "rank"                  : rank,
            "home_rank"             : home_rank,
            "away_rank"             : away_rank,
            "home_profile"          : home_profile,
            "away_profile"          : away_profile,
            "stats_home"            : stats_home,
            "stats_away"            : stats_away,
            "competitionstats"      : competitionstats,
        }
        return ctx






@render_to('fixtureApp/index_test.html')
def features_test(request, ):
    if request.method == "GET":
        # type = TypePrediction.get("1X")
        type = TypePrediction.get("12")
        datas = PredictionTest.objects.filter(is_checked = False, type = type).values_list('match__id')
        matchs = Match.objects.filter(id__in = datas)
        
        ctx = {
            "matchs" : matchs,
        }
        return ctx
    