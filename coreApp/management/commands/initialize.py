from django.core.management.base import BaseCommand, CommandError
from competitionApp.models import TypeCompetition
from settings import settings
from .extract_data import save_from_dir, save_from_file
from bettingApp.models import Bookmaker
from predictionApp.models import *
from statsApp.models import *
from django.contrib.auth.models import User, Group, Permission

import threading
    
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        
        print("Super admin registered")
        user = User(
            username = "admin",
            email = "",
            first_name = "Super",
            last_name = "Administrateur",
        )
        user.set_password("12345678")
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        
        TypeCompetition.objects.get_or_create(
            name = "full",
            etiquette = "FULL"
        )
        TypeCompetition.objects.get_or_create(
            name = "partial",
            etiquette = "PARTIAL"
        )
        
        
        datas = {
            "m1_5":"Moins de 1,5but dans le match",
            "m2_5":"Moins de 2,5buts dans le match",
            "m3_5":"Moins de 3,5buts dans le match",
            "p1_5":"Plus de 1,5but dans le match",
            "p2_5":"Plus de 2,5buts dans le match",
            "p3_5":"Plus de 3,5buts dans le match",
        
            "p0_5_MT":"Plus de 0,5buts à la mi-temps",
            
            "1":"Voictoire de l'equipe à domicile",
            "2":"Voictoire de l'equipe à l'extérieur",
            "1X":"Equipe à domicile ne perd pas",
            "X2":"Equipe à l'exterieur ne perd pas",
            "12":"Pas de nul dans le match",
            "X":"Match nul",
            
            "HG":"But de l'equipe à domicile",
            "HG|2":"Pas plus de 1 But pour l'equipe à domicile",
            "AG":"But de l'equipe à l'exterieur",
            "AG|2":"Pas plus de 1 But pour l'equipe à l'exterieur",
            "btts":"But pour les deux equipes",
            "no_btts":"Les deux équipes ne marquent pas",
            
            "corner_p6_5":"Plus de 8,5 corners dans le match",
            "corner_m12_5":"Moins de 12,5 corners dans le match",
            "1C":"Voictoire de l'equipe à domicile aux corners",
            "2X":"Voictoire de l'equipe à l'extérieur aux corners",
        }
        for x in datas:
            TypePrediction.objects.get_or_create(
                name = x, 
                code = x, 
                description = datas[x], 
            )
            
            

        datas = {
            "M0":"Prédiction sur les stats d'avant match",
            "M1":"Prédiction sur les confrontations directes",
            "M2":"Prédiction sur les ppg",
            "M3":"Prédiction sur les ppg 2",
            "M4":"Prédiction sur les odds betting"
        }
        for x in datas:
            ModePrediction.objects.get_or_create(
                name = x, 
                description = datas[x], 
            )
            
            
            
            

        datas = {            
            "Win":"Victoires",
            "Draw":"match nul",
            "Lose":"Defaites",
            
            "btts":"Les deux équipes marquent",
            "CS":"Clean sheet",
            "GC":"Au moins un but concédé",
            "GS":"Au moins un but marqué",
            
            "p1_5":"Au moins de 2 buts dans le match",
            "m3_5":"Au plus de 3 buts dans le match",
            
            "TGS":"Total des buts marqués",
            "TGC":"Total des buts concédés"
        }
        for x in datas:
            TypeFact.objects.get_or_create(
                name = x, 
                description = datas[x], 
            )
            
            
            
