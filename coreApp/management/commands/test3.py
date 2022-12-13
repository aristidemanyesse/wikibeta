from django.core.management.base import BaseCommand, CommandError
import csv, os, re
from betting.models import *
from fixtureApp.models import *
from dateparser import parse
from django.db.models import Q


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        # datas = EditionCompetition.objects.filter()
        # for edit in datas:
        #     matchs = edit.edition_du_match.filter(deleted = False).order_by("date").exclude(date = None)
        #     print(len(matchs), matchs.first().date, matchs.last().date) 
        #     edit.start_date =   matchs.first().date  
        #     edit.finish_date =   matchs.last().date  
        #     edit.save()
            
        #     # break
        
        
        
        matchs = Match.objects.filter().order_by("-date")
        for match in matchs:
            before_stats(match, match.home)  
            before_stats(match, match.away)  
        
        
        
def before_stats(match:Match, team:EditionTeam): 
    points = 0
    scored = 0
    conceded = 0
    
    befores = Match.objects.filter(date__lt = match.date, edition = match.edition).filter(Q(home=team) | Q(away=team)).order_by("date")
    for m in befores:
        points += m.points_for_this_macth(match.home if (match.home == team) else match.away)
        scored += m.goals_scored(match.home if (match.home == team) else match.away)
        conceded += m.goals_conceded(match.home if (match.home == team) else match.away)
    
    bef, created = BeforeMatchStat.objects.get_or_create(
        match = match,
        team = match.home if (match.home == team) else match.away,
        ppg = round((points / len(befores)), 2) if len(befores) > 0 else 0,
        goals_scored = scored,
        avg_goals_scored = round((scored / len(befores)), 2) if len(befores) > 0 else 0,
        goals_conceded = conceded,
        avg_goals_conceded = round((conceded / len(befores)), 2) if len(befores) > 0 else 0
    )
    
    print(bef, created)