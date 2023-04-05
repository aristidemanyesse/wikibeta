import numpy as np
from django.core.management.base import BaseCommand, CommandError
from bettingApp.models import *
from fixtureApp.models import *
from statsApp.models import *
from competitionApp.models import *
from predictionApp.models import *
from dateparser import parse
import threading
import time
from datetime import datetime, timedelta
        
import numpy as np
from sklearn.linear_model import LinearRegression


class Command(BaseCommand):

    
    
    
        
    def handle(self, *args, **options):
        def predict_Z(X, Y, Z, x_new, y_new):
                # Concaténer les tableaux X et Y en une matrice
            data = np.concatenate((np.atleast_2d(X).T, np.atleast_2d(Y).T), axis=1)

            # Créer un objet de régression linéaire et entraîner le modèle sur les données X et Y
            model = LinearRegression()
            model.fit(data, Z)

            # Prédire la valeur de Z pour les nouvelles valeurs de X et Y données en entrée
            x_new = np.atleast_2d(x_new)
            y_new = np.atleast_2d(y_new)
            new_data = np.concatenate((x_new.T, y_new.T), axis=1)
            z_pred = model.predict(new_data)

            return z_pred
        
        def correlation_coefficient(X, Y, Z):
                # Concaténer les tableaux X, Y et Z en une matrice
            data = np.concatenate((np.atleast_2d(X), np.atleast_2d(Y), np.atleast_2d(Z)), axis=0)

            # Calculer la matrice de corrélation
            corr_matrix = np.corrcoef(data)

            # Extraire le coefficient de corrélation entre les variables Z et les variables X et Y
            corr_Z_X = corr_matrix[0, 2]
            corr_Z_Y = corr_matrix[1, 2]

            return corr_Z_X, corr_Z_Y




        
        for_tab = []
        against_tab =[]
        result_tab = []
        match = Match.objects.filter(is_finished=True).order_by("?").first()
        for team in [match.home, match.away]:
            matches = team.get_last_matchs(match, position = True, edition = True)
            for mx in matches:
                result = mx.get_result()
                pts_h, ppg_h, scored_h, avg_goals_scored_h, conceded_h, avg_goals_conceded_h = mx.home.last_stats(mx, edition = True, number = 7)
                pts_a, ppg_a, scored_a, avg_goals_scored_a, conceded_a, avg_goals_conceded_a = mx.away.last_stats(mx, edition = True, number = 7)
                
                if team == match.home == mx.home:
                    for_tab.append(pts_h)
                    against_tab.append(pts_a)
                    result_tab.append(result.home_score)
                    
                elif team == match.away == mx.away:
                    for_tab.append(pts_h)
                    against_tab.append(pts_a)
                    result_tab.append(result.home_score)
                    
            # i = 0
            # mx = match
            # while i < 7:
            #     try:
            #         mx = team.prev_match(mx)
            #         if team == match.home == mx.home or team == match.away == mx.away:
            #             result = mx.get_result()
            #             pts_h, ppg_h, scored_h, avg_goals_scored_h, conceded_h, avg_goals_conceded_h = mx.home.last_stats(mx, edition = True, number = 7)
            #             pts_a, ppg_a, scored_a, avg_goals_scored_a, conceded_a, avg_goals_conceded_a = mx.away.last_stats(mx, edition = True, number = 7)
                        
            #             for_tab.append(avg_goals_scored_h)
            #             against_tab.append(avg_goals_conceded_a)
            #             result_tab.append(result.home_score)
            #             i += 1
            #     except Exception as e:
            #         print("Error")
                    

            # Création des tableaux x, y et z
            x = np.array(for_tab)
            y = np.array(against_tab)
            z = np.array(result_tab)
        #     # x = np.array([1, 2, 3, 4, 5])
        #     # y = np.array([2, 4, 6, 8, 10])
        #     # z = np.array([3, 5, 7, 9, 11])

        #     # Création du tableau de données
        #     data = np.column_stack((x, y, z))

        #     # Calcul des coefficients de la surface de régression
        #     coefficients = np.polyfit(data[:,0], data[:,1], 1)
        #     # Affichage de la valeur prédite
        #     print("X========", x)
        #     print("Y========", y)
        #     print("Z========", z)

        #     # Définition de la fonction de prédiction
        #     def predict_value(x_value, y_value, coefficients):
        #         z_value = np.polyval(coefficients, x_value)
        #         return z_value
            
 

            # x = np.array([1, 2, 3, 4, 5])
            # y = np.array([2, 4, 6, 8, 10])
            # z = np.array([3, 5, 7, 9, 11])
            
            result = match.get_result()
            pts_h, ppg_h, scored_h, avg_goals_scored_h, conceded_h, avg_goals_conceded_h = match.home.last_stats(match, edition = True, number = 7)
            pts_a, ppg_a, scored_a, avg_goals_scored_a, conceded_a, avg_goals_conceded_a = match.away.last_stats(match, edition = True, number = 7)
            
            test, = predict_Z(x, y, z,  pts_h, pts_a)
            print(test, result.home_score if team == match.home else result.away_score)
            test = correlation_coefficient(x, y, z)
            print("coorelation", test[0])