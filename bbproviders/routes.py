import requests
from competitionApp.models import *
from ..providers.management.commands.headers import *
from difflib import SequenceMatcher



def get_day_matchs(day, month, year):
    url = "https://footapi7.p.rapidapi.com/api/matches/{}/{}/{}".format(day, month, year)
    response = requests.request("GET", url, headers=headers)
    return datas

def get_live_matchs():
    url = "https://footapi7.p.rapidapi.com/api/matches/live"
    response = requests.request("GET", url, headers=headers)
    return datas

def get_match_odds(id):
    url = "https://footapi7.p.rapidapi.com/api/match/{}/odds".format(id)
    response = requests.request("GET", url, headers=headers)
    return datas
