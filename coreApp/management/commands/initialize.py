from django.core.management.base import BaseCommand, CommandError
import os, time
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
        
        
        datas = {
            "m1_5":"Moins de 1,5but dans le match",
            "m2_5":"Moins de 2,5buts dans le match",
            "m3_5":"Moins de 3,5buts dans le match",
            "p1_5":"Plus de 1,5but dans le match",
            "p2_5":"Plus de 2,5buts dans le match",
            "p3_5":"Plus de 3,5buts dans le match",
            "VN_Home":"Equipe à domicile ne perd pas",
            "VN_Away":"Equipe à l'exterieur ne perd pas",
            "12":"Pas de nul dans le match",
            "But_Home":"But de l'equipe à domicile",
            "But_Away":"But de l'equipe à l'exterieur",
            "btts":"But pour les deux equipes",
            "no_btts":"Les deux équipes ne marquent pas",
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