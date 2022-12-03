from django.shortcuts import render
from django.shortcuts import get_object_or_404
import datetime
from .models import *
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
        print(competition)
        ctx = {"competition" : competition}
        return render(request, "features/competition.html", ctx)
      
        
def team(request, name):
    if request.method == "GET":
        team = Team.objects.get(name = name)
        print(team)
        ctx = {"team" : team}
        return render(request, "features/team.html", ctx)
        

  
def match(request, id):
    if request.method == "GET":
        match = Match.objects.all().first()
        print(match)
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