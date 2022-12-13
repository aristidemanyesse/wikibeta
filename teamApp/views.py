from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from annoying.decorators import render_to
from django.http import HttpResponseRedirect
from .models import *
from teamApp.models import *
from competitionApp.models import *
# Create your views here.



               
def team(request, name):
    if request.method == "GET":
        team = Team.objects.get(name = name)
        editions = team.team_edition.filter()
        edition = editions.first()
        return HttpResponseRedirect(reverse('teamApp:team_edition', args=[team.name, edition.edition.edition.name]))
        

@render_to("teamApp/team.html")
def team_edition(request, name, edition):
    if request.method == "GET":
        pre = EditionTeam.objects.filter(team__name = name, edition__edition__name = edition).order_by("-edition__edition__name")
        team = pre.first()
        editions = team.team.team_edition.filter()
        matchs = Match.objects.filter(Q(home = team) | Q(away = team)).order_by("-date")
        matchs_joues = matchs[:20]
        
        ctx = {
            "team":team.team, 
            "editions":editions, 
            "matchs":matchs, 
            "matchs_20":matchs_joues, 
            }
        return ctx