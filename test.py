import numpy as np
from scipy.stats import poisson, skellam

# Moyennes de buts marqués pour chaque équipe
home_goals_mean = 3
away_goals_mean = 1.2

# Calculer les probabilités de chaque score possible
score_proba = np.zeros((10, 10))
for i in range(10):
    for j in range(10):
        score_proba[i, j] = poisson.pmf(i, home_goals_mean) * poisson.pmf(j, away_goals_mean)

# Obtenir les scores dont la probabilité est supérieure à 0.01 et les trier par ordre décroissant de probabilité
scores = [(i, j, score_proba[i, j]) for i in range(10) for j in range(10) if score_proba[i, j] > 0.01]
scores_sorted = sorted(scores, key=lambda x: x[2], reverse=True)

# Calculer la probabilité d'avoir un écart de buts donné
skellam_proba = skellam.pmf(np.arange(-10, 11), home_goals_mean, away_goals_mean)
home_win_proba = np.sum(skellam_proba[11:])
away_win_proba = np.sum(skellam_proba[:10])
draw_proba = skellam_proba[10]

# Afficher les résultats en pourcentage
print(f"Probabilité de victoire à domicile : {home_win_proba*100:.2f}%")
print(f"Probabilité de match nul : {draw_proba*100:.2f}%")
print(f"Probabilité de victoire à l'extérieur : {away_win_proba*100:.2f}%")

# Afficher les scores avec leur probabilité
print("Scores les plus probables :")
for score in scores_sorted:
    if score[2] > 0.01:
        for i, proba in enumerate(skellam_proba):
            if proba > 0.05 and i-10 == score[0]-score[1]:
                print(f"{score[0]}-{score[1]} : {score[2]*100:.2f}% avec {i-10}: {proba:.2%}")
                break



# # Afficher les résultats
# print("Probabilité d'avoir un écart de buts de:")
# for i, proba in enumerate(skellam_proba):
#     if proba > 0.05:
#         print(f"{i-10}: {proba:.2%}")