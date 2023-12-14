from math import sqrt
from django.core.management.base import BaseCommand, CommandError
from bettingApp.models import *
from coreApp.management.commands.predictionscore import predictscore
from coreApp.templatetags import footstats
from fixtureApp.models import *
from statsApp.models import *
from competitionApp.models import *
from predictionApp.models import *


# def determiner_categorie(dynamisme, attaque, defense, maitrise):
#     if all(note >= 17 for note in [dynamisme, attaque, defense, maitrise]):
#         return "Champions Légendaires"
#     elif all(note >= 15 for note in [dynamisme, attaque, defense, maitrise]):
#         return "Cyborg"
#     elif all(note >= 13.5 for note in [dynamisme, attaque, defense, maitrise]):
#         return "Équipes Étoiles"
#     elif all(note >= 12 for note in [dynamisme, attaque, defense, maitrise]):
#         return "Compétiteurs Acharnés"
#     elif (dynamisme >= 14 and attaque >= 14) and (defense < 14 or maitrise < 14):
#         return "Attaquants Foudroyants"
#     elif (defense >= 14 and maitrise >= 14) and (dynamisme < 14 or attaque < 14):
#         return "Murailles Impénétrables"
#     elif any(note >= 16 for note in [dynamisme, attaque, defense, maitrise]) and all(note >= 11 for note in [dynamisme, attaque, defense, maitrise]):
#         return "Spécialistes Tactiques"
#     elif all(note >= 10 for note in [dynamisme, attaque, defense, maitrise]):
#         return "Équipes en Ascension"
#     elif all(note >= 8 for note in [dynamisme, attaque, defense, maitrise]):
#         return "Débrouillard"
#     elif all(note >= 6 for note in [dynamisme, attaque, defense, maitrise]):
#         return "Équipe Malade"
#     elif all(note >= 3 for note in [dynamisme, attaque, defense, maitrise]):
#         return "Tocard"
#     else:
#         return "Vaurien Ultime"


def determiner_categorie(dynamisme, attaque, defense, maitrise):
    if attaque >= 14 and dynamisme >= 14 and maitrise >= 8:
        return "Attaque Totale"
    elif dynamisme >= 12 and defense >= 10 and attaque >= 6:
        return "Contre-Attaque Rapide"
    elif maitrise >= 12 and attaque >= 10 and defense >= 8:
        return "Jeu de Position"
    elif defense >= 12 and maitrise >= 10 and dynamisme >= 6:
        return "Défense Solide"
    elif dynamisme >= 12 and maitrise >= 10 and defense >= 8:
        return "Pressing Haut"
    elif defense >= 10 and attaque >= 10 and dynamisme >= 6:
        return "Jeu Aérien et Physique"
    elif maitrise >= 12 and dynamisme >= 10 and (attaque >= 8 or defense >= 8):
        return "Polyvalence Tactique"
    elif maitrise >= 5 and attaque >= 4 and dynamisme >= 3:
        return "Équipes en Reconstruction"
    elif dynamisme >= 3 and defense >= 3 and maitrise <= 8:
        return "Combattants Déterminés"
    else:
        return "Non Classifiable"


class Command(BaseCommand):
    
    def handle(self, *args, **options):

        coul = 0 
        tout = 0
        total = 0
        PredictionTest.objects.all().delete()            
        for match in Match.objects.filter(is_finished = True).order_by("-date")[:1000]: 
            # home_stats = match.get_home_before_stats()
            # away_stats = match.get_away_before_stats()
            
            home = match.home.get_team_profile(match)
            home_maitrise = match.home.maitrise(match)
            
            away = match.away.get_team_profile(match)
            away_maitrise = match.away.maitrise(match)
            
            home_rank = LigneRanking.objects.filter(team = match.home, ranking__date__lte = match.date).order_by('-ranking__date').first()
            away_rank = LigneRanking.objects.filter(team = match.away, ranking__date__lte = match.date).order_by('-ranking__date').first()
            
            # compet =  match.edition.edition_stats.filter(ranking__date__lte = match.date).first()
            
            if home is None or away is None:
                continue
            
            cats = []
            # for profile in [home, away]:
            #     cat = determiner_categorie(profile.dynamique, profile.attack, profile.defense, match.home.maitrise(match) if home == profile else  match.away.maitrise(match))
            #     cats.append(cat)
            
            # print(cats[0] + " VS " + cats[1])
            result = match.get_result()
            print(result)
            # print(result, away.defense)
            # print("")
            # scores_exacts = predictscore(match)
                

            # if home_maitrise >= away_maitrise + 4 and home.attack >= away.attack + 3:
            #     PredictionTest.objects.create(
            #         mode = ModePrediction.get("M2"),
            #         type = TypePrediction.get("1X"),
            #         match = match,
            #         pct = 85
            #     )

            
            if home_maitrise > 10 and away_maitrise > 10:
                PredictionTest.objects.create(
                    mode = ModePrediction.get("M0"),
                    type = TypePrediction.get("m3_5"),
                    match = match,
                    pct = 85
                )
            else:
                PredictionTest.objects.create(
                    mode = ModePrediction.get("M4"),
                    type = TypePrediction.get("p1_5"),
                    match = match,
                    pct = 85
                )

            # if home.dynamique <= away.dynamique and home.attack <= away.attack:
            #     PredictionTest.objects.create(
            #         mode = ModePrediction.get("M0"),
            #         type = TypePrediction.get("X2"),
            #         match = match,
            #         pct = 85
            #     )
            
            
            # tab_def = {}
            # tab_atk = {}
            # tab_dyn = {}
            # for i, mat in enumerate(match.home.get_last_matchs(match, number = 6, edition = True)):
            #     result = mat.get_result()
            #     print(result)
            # for i, mat in enumerate(match.away.get_last_matchs(match, number = 6, edition = True)):
            #     result = mat.get_result()
            #     print(result)
            #     if mat.home == match.home:
            #         print(mat.home)
            #         away = mat.away.get_team_profile(mat)
            #         tab_def[str(away.defense)] = result.home_score
            #         tab_atk[str(away.attack)] = result.away_score
            #         tab_dyn[str(away.dynamique)] = result.home_score
            #     elif mat.away == match.home:
            #         print(mat.away)
            #         home = mat.home.get_team_profile(mat)
            #         tab_def[str(home.defense)] = result.away_score
            #         tab_atk[str(home.attack)] = result.home_score
            #         tab_dyn[str(home.dynamique)] = result.away_score
                
            # print(tab_def)
            # print(tab_atk)
            # print(tab_dyn)
            # break
     
            print("DYN", "\t", round(home.dynamique, 2), "\t", round(away.dynamique, 2))
            print("ATK", "\t", round(home.attack, 2), "\t", round(away.attack, 2))
            print("DEF", "\t", round(home.defense, 2), "\t", round(away.defense, 2))
            print("MAI", "\t", home_maitrise , "\t", away_maitrise)
            print("RAN", "\t", home_rank.level , "\t", away_rank.level)
            print("PTS", "\t", home_rank.pts , "\t", away_rank.pts)
            print("--------------------------------------------")
            print("")
                
        # print(coul, total, tout)