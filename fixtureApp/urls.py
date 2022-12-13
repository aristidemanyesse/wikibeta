
from django.shortcuts import redirect
from django.urls import path

from . import views

app_name = "fixtureApp"
urlpatterns = [
    path('', views.home, name="home"),
    path('match/<uuid:id>/', views.match, name="match"),
]