from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
import datetime
from django.http import HttpResponseRedirect
from .models import *
from core.functions import *
# Create your views here.


def home(request):
    if request.method == "GET":
        ctx = {}
        return render(request, "features/index.html", ctx)
        
        
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
        return HttpResponseRedirect(reverse('features:competition_edition', args=[pays, competition.name, edition.edition]))
      
 
 
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
      
               

               
def team(request, name):
    if request.method == "GET":
        team = Team.objects.get(name = name)
        editions = team.team_edition.filter()
        edition = editions.first()
        return HttpResponseRedirect(reverse('features:team_edition', args=[team.name, edition.edition.edition.name]))
        


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
        return render(request, "features/team.html", ctx)
        

    
def match(request, id):
    if request.method == "GET":
        match = Match.objects.get( id = id)
        
        matchs = match.similaires_ppg()
        # for x in matchs:
        #     print(x, x.score())
        
        total = 0
        if len(matchs) > 0:
            for x in matchs:
                ppg_home = x.get_home_before_stats().ppg
                ppg_away = x.get_away_before_stats().ppg
                
                if ppg_home == ppg_away :
                    total += 1
                elif ppg_home > ppg_away and x.home_score >= x.away_score :
                    total += 1
                elif ppg_home < ppg_away and x.home_score <= x.away_score :
                    total += 1
                
            moy = total / len(matchs)
                    
            print("moyenne ::::::", moy)
            print("pre 1.5  ===>", fish_law_moins(moy, 1.5))
            print("Oui  ===>", fish_law_favoris_vn(moy, 1.5))
        ctx = {"match" : match}
        return render(request, "features/match.html", ctx)



def stats(request, id):
    if request.method == "GET":
        return render(request, "features/match.html")
           
           
def predictions(request, id):
    if request.method == "GET":
        return render(request, "features/match.html")
           
           
def forum(request, id):
    if request.method == "GET":
        return render(request, "features/match.html")
           
# def clients(request):
#     if request.method == "GET":
#         GroupeCommande.maj_etat()
#         date = datetime.datetime.now() - datetime.timedelta(days=7)
        
#         clients = Client.objects.filter(deleted = False)
#         if request.module_name != "manager":
#             clients = clients.filter(agence = request.agence)
            
#         ctx = {
#             "clients" : clients,
#             "clients_semaine" : clients.filter(created_at__gte = date ),
#             "types" : TypeClient.objects.filter(deleted = False)
#         }
#         return render(request, "clients/pages/clients.html", ctx)
        



# def client(request, client_id):
#     try:
#         del request.session["groupecommande_id"]
#     except Exception as e:
#         print("view de client :", e)

#     if request.method == "GET":
#         client = get_object_or_404(Client, pk = client_id)
#         request.session["client_id"] = str(client.id)

#         datas = []
#         for groupe in client.get_groupecommandes():
#             commandes = groupe.commande_groupecommande.filter(deleted = False)
#             livraisons = groupe.groupecommande_livraison.filter(deleted = False).exclude(etat__etiquette = Etat.ANNULE)

#             for commande in commandes:
#                 commande.tipe = "commande"
#             for livraison in livraisons:
#                 livraison.tipe = "livraison"

#             mylist = []
#             mylist.extend(commandes)
#             mylist.extend(livraisons)
#             mylist.sort(key=lambda x: x.created_at)
#             datas.append({
#                 "groupe":groupe,
#                 "commandes": commandes,
#                 "livraisons": livraisons,
#                 "livraisons_encours": groupe.groupecommande_livraison.filter(deleted = False, etat__etiquette = Etat.EN_COURS),
#                 "sort_lignes": mylist,
#                 "briques" : groupe.all_briques()
#             })

#         items = []
#         for item in ReglementCommande.objects.filter(commande__groupecommande__client = client, deleted = False):
#             items.append(item.mouvement)
#         for item in CompteClient.objects.filter(client = client, deleted = False):
#             if item.mouvement not in items:
#                 items.append(item.mouvement)
#         items.sort(key=lambda x: x.created_at)

#         context = {
#             'client' : client,
#             'clients' : Client.objects.filter(agence = request.agence),
#             'types' : TypeClient.objects.filter(deleted = False),
#             "datas" : datas,
#             "briques" : Brique.objects.filter(active = True, deleted = False),
#             'commandes' : GroupeCommande.objects.filter(etat__etiquette = Etat.EN_COURS),

#             "chauffeurs": Chauffeur.objects.filter(deleted = False, agence = request.agence),
#             "vehicules": Vehicule.objects.filter(deleted = False, agence = request.agence),
#             "modepayements": ModePayement.objects.filter(deleted = False),
#             "zonelivraisons": ZoneLivraison.objects.filter(deleted = False, agence = request.agence),
#             "modelivraisons": ModeLivraison.objects.filter(deleted = False),
#             "mouvements": items,

#         }
#         return render(request, "clients/pages/client.html", context)