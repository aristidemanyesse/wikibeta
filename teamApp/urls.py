
from django.shortcuts import redirect
from django.urls import path

from . import views

app_name = "teamApp"
urlpatterns = [
    path('<str:name>/', views.team, name="team"),
    path('<str:name>/<str:edition>/', views.team_edition, name="team_edition"),
]