from django.shortcuts import render, reverse
from competitionApp.models import *
from django.http import HttpResponseRedirect
from annoying.decorators import render_to
import statsApp.get_recherche_facts as get_recherche_facts
from datetime import datetime
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
        edition = EditionCompetition.objects.get(competition__pays__name = pays, competition__name = competition, edition__name = edition)
        competition = edition.competition
        editions = [] or competition.competition_edition.filter()
        matchs_played = edition.edition_du_match.filter(is_finished = True).exclude(is_posted = True).order_by('-date')
        next_matchs = edition.edition_du_match.filter(is_finished = False, date__gte = datetime.now())
        
        rank = edition.edition_rankings.filter().order_by('-date').first()
        
        teams = edition.edition_team.filter()
        total_official_matchs = (len(teams)-1) * len(teams)
        ratio = round(total_official_matchs / len(matchs_played) ) * 100
        
        facts = [] 
        # or get_recherche_facts.function(matchs)
        
        victoires = nuls = p1_5 = m3_5 = btts = cs = ht = ft = 0
        for x in matchs_played:
            result = x.get_result()
            if result.home_half_score is not None:
                ht += result.home_half_score + result.away_half_score
                ft += (result.home_score + result.away_score) - (result.home_half_score + result.away_half_score )
                
            if result.home_score != result.away_score:
                victoires += 1
            else :
                nuls += 1
                
            if result.home_score > 0 and result.away_score > 0:
                btts += 1
            else :
                cs += 1
                
            if result.home_score + result.away_score > 1.5:
                p1_5 += 1
            elif result.home_score + result.away_score < 3.5 :
                m3_5 += 1

        
        ctx = {
            "edition":edition,
            "editions":editions,
            "competition" : competition,
            "matchs": matchs_played, 
            "next_matchs": next_matchs, 
            "total_official_matchs": total_official_matchs,
            "teams":teams, 
            "facts":facts, 
            "rank":rank, 
            "matchs20":matchs_played[:20], 
            "ratio":ratio, 
            "victoires": victoires,
            "nuls": nuls,
            "p1_5": p1_5,
            "m3_5": m3_5,
            "btts": btts,
            "cs": cs,
            "ht": ht,
            "ft": ft,
            }
        return ctx
      