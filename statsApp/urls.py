
from django.shortcuts import redirect
from django.urls import path

from . import views

app_name = "statsApp"
urlpatterns = [
    path('', views.statistiques, name="statistiques"),
]