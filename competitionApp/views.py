from django.shortcuts import render, reverse
from competitionApp.models import *
from django.http import HttpResponseRedirect
from annoying.decorators import render_to

# Create your views here.


@render_to("competitionApp/pays.html")
def pays(request):
    if request.method == "GET":
        pays = Pays.objects.all()
        ctx = {"pays" : pays}
        return ctx
    
        
@render_to("competitionApp/country.html")
def country(request, pays):
    if request.method == "GET":
        country = Pays.objects.get(name = pays)
        ctx = {"country" : country}
        return ctx
        
        
        
def competition(request, pays, competition):
    if request.method == "GET":
        competition = Competition.objects.get(pays__name = pays, name = competition)
        editions = competition.competition_edition.filter()
        edition = editions.first()
        return HttpResponseRedirect(reverse('competitionApp:competition_edition', args=[pays, competition.name, edition.edition]))
      
 
 
@render_to("competitionApp/competition.html")
def competition_edition(request, pays, competition, edition):
    if request.method == "GET":
        edition = [] or  EditionCompetition.objects.get(competition__pays__name = pays, competition__name = competition, edition__name = edition)
        competition = edition.competition
        editions = [] or competition.competition_edition.filter()
        matchs_joues = []
        # matchs_joues = edition.edition_du_match.filter().order_by("-date")
        teams = [] or edition.edition_team.filter()
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
        return ctx
      