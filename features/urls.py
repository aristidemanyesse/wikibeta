
from django.shortcuts import redirect
from django.urls import path

from . import views

app_name = "features"
urlpatterns = [
    path('', views.home, name="home"),
    path('pays/', views.pays, name="pays"),
    path('pays/<str:pays>/', views.country, name="country"),
    path('pays/<str:pays>/<str:competition>/', views.competition, name="competition"),
    path('pays/<str:pays>/<str:competition>/<str:edition>/', views.competition_edition, name="competition_edition"),
    path('team/<str:name>/', views.team, name="team"),
    path('team/<str:name>/<str:edition>/', views.team_edition, name="team_edition"),
    path('match/<uuid:id>/', views.match, name="match"),
    
    
    path('stats/', views.stats, name="stats"),
    path('predictions/', views.predictions, name="predictions"),
    path('forum/', views.forum, name="forum"),


    # path('ajax/crediter/', ajax.crediter),
    # path('ajax/rembourser/', ajax.rembourser),
    # path('ajax/regler_toutes_dettes/', ajax.regler_toutes_dettes),
]