from django.shortcuts import render
from competitionApp.models import *
from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

# Create your views here.


def pays(request):
    if request.method == "GET":
        pays = Pays.objects.all()
        ctx = {"pays" : pays}
        return render(request, "features/pays.html", ctx)
    
        
def country(request, pays):
    if request.method == "GET":
        country = Pays.objects.get(name = pays)
        print(country)
        ctx = {"country" : country}
        return render(request, "features/country.html", ctx)
        
        
        
def competition(request, pays, competition):
    if request.method == "GET":
        competition = Competition.objects.get(pays__name = pays, name = competition)
        editions = competition.competition_edition.filter()
        edition = editions.first()
        return HttpResponseRedirect(reverse('fixtureApp:competition_edition', args=[pays, competition.name, edition.edition]))
      
 
 
def competition_edition(request, pays, competition, edition):
    if request.method == "GET":
        edition = EditionCompetition.objects.get(competition__pays__name = pays, competition__name = competition, edition__name = edition)
        competition = edition.competition
        editions = competition.competition_edition.filter()
        matchs_joues = edition.edition_du_match.filter().order_by("-date")
        teams = edition.edition_team.filter()
        total_matchs = (len(teams)-1) * len(teams)
        ratio = round(len(matchs_joues) / total_matchs ) * 100
        
        ctx = {
            "edition":edition,
            "matchs":matchs_joues, 
            "matchs_20":matchs_joues[:20], 
            "nb_matchs":total_matchs, 
            "ratio":ratio, 
            "teams":teams, 
            "editions":editions,
            "competition" : competition
            }
        return render(request, "features/competition.html", ctx)
      