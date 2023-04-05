import numpy as np
import pandas as pd
import math
from django.db.models import Avg
from django.core.management.base import BaseCommand
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from fixtureApp.models import Match


class Command(BaseCommand):
    help = 'Train neural network to predict goals in football matches'

    def handle(self, *args, **options):
        # Load data from Django models
        matches = Match.objects.all()

        # Preprocess data
        data = []
        for match in matches:
            home_stats = match.get_home_before_stats()
            away_stats = match.get_away_before_stats()
            min_points = min(home_stats.points, away_stats.points)
            

            pts, ppg, scored, avg_goals_scored_h, conceded, avg_goals_conceded_h = match.home.last_stats(match, edition = True, number = 5)
            pts, ppg, scored, avg_goals_scored_a, conceded, avg_goals_conceded_a = match.away.last_stats(match, edition = True, number = 5)

            
            home_team = match.home_team
            away_team = match.away_team
            home_goals = match.home_goals
            away_goals = match.away_goals
            total_goals = home_goals + away_goals
            home_team_mean_goals = Match.objects.filter(home_team=home_team).aggregate(avg_goals=Avg('home_goals'))['avg_goals']
            away_team_mean_goals = Match.objects.filter(away_team=away_team).aggregate(avg_goals=Avg('away_goals'))['avg_goals']
            
            data.append([home_team_mean_goals, away_team_mean_goals, total_goals, home_goals, away_goals])

        # Convert data to numpy arrays
        data = np.array(data)
        X = data[:, :2]  # Features: Home team mean goals and away team mean goals
        y = data[:, 2:]  # Labels: Total goals, home goals, away goals

        # Split data into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        # Define neural network model
        model = Sequential()
        model.add(Dense(16, input_dim=2, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(3))

        # Compile model
        model.compile(loss='mse', optimizer='adam')

        # Train model
        batch_size = 256
        epochs = 50
        model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(X_val, y_val))

        # Evaluate model on validation set
        val_loss, val_mae, val_mse = model.evaluate(X_val, y_val)
        print(f'Validation loss: {val_loss}, Validation mean absolute error: {val_mae}, Validation mean squared error: {val_mse}')

        # Make predictions on test set
        predictions = model.predict(X_val)

        # Print predictions
        for i, prediction in enumerate(predictions):
            home_goals_pred, away_goals_pred, total_goals_pred = prediction
            home_goals_true, away_goals_true, total_goals_true = y_val[i]
            print(f'Home goals prediction: {home_goals_pred:.2f}, Home goals true: {home_goals_true:.2f}')
            print(f'Away goals prediction: {away_goals_pred:.2f}, Away goals true: {away_goals_true:.2f}')
            print(f'Total goals prediction: {total_goals_pred:.2f}, Total goals true: {total_goals_true:.2f}')




# def factorial(n):
#     if n < 0:
#         return None
#     elif n == 0:
#         return 1
#     else:
#         return n * factorial(n-1)



# def predict_goals_for_team(mean_goals_scored, mean_goals_conceded_opponent):
    
#     # On calcule la probabilité que l'équipe marque 0 buts
#     p_zero_goals = np.exp(-mean_goals_scored) * np.power(mean_goals_conceded_opponent, 0) / factorial(0)
    
#     # On calcule la probabilité que l'équipe marque au moins 1 but
#     p_at_least_one_goal = 1 - p_zero_goals
    
#     # On calcule le nombre de buts moyen que l'équipe pourrait marquer
#     expected_goals = mean_goals_scored * p_at_least_one_goal
    
#     return expected_goals




# def moyenne_but(atk, defe):
#     atk = round(atk, 1)
#     defe = round(defe, 1)
    
#     if atk == defe:
#         avg = atk + (defe / 2)
        
#     elif atk - defe >= 2:
#         avg = defe + (defe / (atk - defe))
        
#     elif atk - defe > 0:
#         avg = defe + ((atk - defe) / 2)
        
#     elif defe - atk >= 2 :
#         avg =  atk + ((2 * atk ) / defe)
        
#     elif defe - atk > 0 :
#         avg =  atk / defe
        
#     return avg



# def calc_goals_scored(avg_goals_scored, avg_goals_conceded):
#     return avg_goals_scored * (avg_goals_conceded / 2)



# # def poisson_bimodale(a, b, p, k):
# #     lambda_1 = a + b*(1-p)
# #     lambda_2 = a + b*p
# #     prob = (math.pow(lambda_1, k) / math.factorial(k)) * math.exp(-lambda_1) * (1-p + p*math.exp(-lambda_2))**k
# #     return prob*100


# def bimodal_poisson(lambda_1, lambda_2, p, k):
#     prob = p*math.exp(-lambda_1)*(lambda_1**k)/math.factorial(k) + (1-p)*math.exp(-lambda_2)*(lambda_2**k)/math.factorial(k)
#     return prob*100




# a = 1.1
# b = 1.9

# # print(moyenne_but(a, b))
# # print(calc_goals_scored(a, b))
# # predict_goals_for_team(a, b)

# for i in [0, 1, 2, 3, 4, 5]:
#     print(i, "==", bimodal_poisson(a, b, 0, i))
#     print("---------------------------------------")


# def calcul_p(a , b):
#     if a >= b:
#         t = (a-b)/(a+b)
#         return 0.5 + (t / 2)
#     else:
#         t = a / (a +b)
#         return t



# print(calcul_p(a, b))
# print(calcul_p(b, a))
# print(calcul_p(a, b) + calcul_p(b, a))