
from django.shortcuts import redirect
from django.urls import path

from . import views

app_name = "competitionApp"
urlpatterns = [
    path('', views.pays, name="pays"),
    path('<str:pays>/', views.country, name="country"),
    path('<str:pays>/<str:competition>/', views.competition, name="competition"),
    path('<str:pays>/<str:competition>/<str:edition>/', views.competition_edition, name="competition_edition"),

]