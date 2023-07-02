import numpy as np
import pandas as pd
import math
from django.db.models import Avg
from django.core.management.base import BaseCommand
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.metrics import accuracy_score
from fixtureApp.models import Match

import predictionApp.functions.p0 as p0
import predictionApp.functions.p1 as p1
import predictionApp.functions.p2 as p2
import predictionApp.functions.p3 as p3
import predictionApp.functions.p4 as p4
from competitionApp.models import *
from predictionApp.models import *

import statsApp.get_home_facts as get_home_facts
import statsApp.get_away_facts as get_away_facts
import math
import threading
import os, time
import numpy as np
from scipy.stats import poisson, skellam



class Command(BaseCommand):
    help = 'Train neural network to predict goals in football matches'

    def handle(self, *args, **options):
        
        for competition in Competition.objects.all():
            print(competition.__dict__)

            # matches = Match.objects.filter(is_finished = True, edition__competition =  competition).order_by('date')[:2000]
            # data = []
            # for match in matches:
            #     result = match.get_result()
if result is None:
                test += 1
                continue
            #     odds = match.get_odds()
            #     pts_h, ppg_h, scored_h, avg_goals_scored_h, conceded_h, avg_goals_conceded_h = match.home.last_stats(match, edition = True, number = 10)
            #     pts_a, ppg_a, scored_a, avg_goals_scored_a, conceded_a, avg_goals_conceded_a = match.away.last_stats(match, edition = True, number = 10)
                
            #     p1_5 = result.home_score + result.away_score > 1.5
            #     m3_5 = result.home_score + result.away_score < 3.5
            #     btts = result.home_score > 0 and  result.away_score > 0
                
            #     total = result.home_score + result.away_score
            #     data.append([avg_goals_scored_h, avg_goals_conceded_a, avg_goals_scored_a, avg_goals_conceded_h, total])

            # with open("./data2.json", "w") as file:
            #     file.write(json.dumps(data))
            
            
            with open("./data2.json", "r") as file:
                data = json.loads(file.read())

            data = np.array(data)
            X = data[:, :-1]  # Features: Home team mean goals and away team mean goals
            y = data[:, -1:]  # Labels: Total goals, home goals, away goals
            # Split data into training and validation sets
            X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.05, random_state=42)
            

            # Define neural network model
            model = Sequential()
            model.add(Dense(1024, activation='relu', input_shape=(4,)))
            model.add(Dense(16, activation='relu'))
            model.add(Dense(1, activation='relu'))


            # Compile & Train model
            model.compile(loss='mse', optimizer='adam', metrics=['mae', 'mse'])
            model.fit(X_train, y_train, batch_size=32, epochs=50, validation_data=(X_val, y_val))

            # Sauvegarder le modèle
            model.save('./modeles/example.h5')


            # Evaluate model on validation set
            val_loss, val_mae, val_mse = model.evaluate(X_val, y_val)
            print(f'Validation loss: {val_loss}, Validation mean absolute error: {val_mae}, Validation mean squared error: {val_mse}')

            # Make predictions on test set
            predictions = model.predict(X_val)
            predictions = np.round(predictions, 1)
            
            p = t = 0
            # Print predictions
            for i, prediction in enumerate(predictions):  
                # Home_p, Away_p, Total_p, p1_5_p, m3_5_p, btts_p = prediction
                # Home_t, Away_t, Total_t, p1_5_t, m3_5_t, btts_t = y_val[i]
                
                # print(" Home | Away | Total | p1_5 | m3_5 | btts")
                # print(f" {Home_t} | {Away_t} | {Total_t} | {p1_5_t} | {m3_5_t} | {btts_t}")
                # print(f" {Home_p:.2f} | {Away_p:.2f} | {Total_p:.2f} | {p1_5_p:.2f} | {m3_5_p:.2f} | {btts_p:.2f}")
                # print("---------------------------------------------------------------")
                
                
                # p1_5_p, m3_5_p, btts_p = prediction
                # p1_5_t, m3_5_t, btts_t = y_val[i]
                
                # print(" p1_5 | m3_5 | btts")
                # print(f"{p1_5_t} | {m3_5_t} | {btts_t}")
                # print(f"{p1_5_p:.2f} | {m3_5_p:.2f} | {btts_p:.2f}")
                # print("---------------------------------------------------------------")
                
                
                total_t, = y_val[i]
                total_p, = prediction
                if total_p >= 2.8 :
                    t += 1
                    if total_t > 1.5:
                        p += 1
                print("total")
                print(f"{total_t}")
                print(f"{total_p}")
                print("---------------------------------------------------------------")


            # Affichage des résultats
            
            print('total :', p , t)
            print('Pct :', round((p / t) * 100, 2))
            print('Perte (loss) sur l\'ensemble de test :', val_loss)
            print('MAE sur l\'ensemble de test :', val_mae)
            print('MSE sur l\'ensemble de test :', val_mse)
            
            # # calculer le taux de classification correcte
            # accuracy = accuracy_score(y_val, predictions)

            # # afficher le pourcentage de précision
            # print(f"Pourcentage de précision : {accuracy*100:.2f}%")
            
            
            break

