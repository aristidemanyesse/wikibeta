
from django.shortcuts import redirect
from django.urls import path, re_path
from . import views

app_name = "statsApp"
urlpatterns = [
    path('', views.statistiques, name="statistiques"),
    path('test/', views.statistiquestest, name="statistiquestest"),
    re_path(r"^rechercher/cote/(?P<home>\d+\.\d+)/(?P<away>\d+\.\d+)/(?P<draw>\d+\.\d+)/$", views.rechercher_cote, name="rechercher_cote"),
    re_path(r"^rechercher/ppg/(?P<home>\d+\.\d+)/(?P<away>\d+\.\d+)/$", views.rechercher_ppg, name="rechercher_ppg"),
    re_path(r"graphtest", views.test, name="graphtest"),
]