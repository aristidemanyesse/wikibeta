from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from annoying.decorators import render_to
from django.http import HttpResponseRedirect
from .models import *
from coreApp.functions import *
from predictionApp.models import *
# Create your views here.


@render_to('fixtureApp/index.html')
def home(request):
    if request.method == "GET":
        ctx = {}
        return ctx
        


@render_to('fixtureApp/match.html')
def match(request, id):
    if request.method == "GET":
        match = Match.objects.filter(is_finished=False)
        confrontations = match.confrontations_directes()
        predictions = match.prediction_match.filter()

        ctx = {
            "matchs" : matchs,
            "confrontations" : confrontations[:10],
            "predictions" : predictions,
        }
        return ctx
