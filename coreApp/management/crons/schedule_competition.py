from competitionApp.models import *
import datetime
from django.db.models import Avg, Sum, Q

def handle():
    try:   
        print("--------------------------------", datetime.datetime.now()) 
        for item in EditionCompetition.objects.filter(is_finished = False).order_by("edition__name"):
            matchs = item.edition_du_match.filter(deleted = False).exclude(date = None).order_by("date")
            if len(matchs) > 0:
                item.start_date = matchs.first().date
                item.finish_date = matchs.last().date
                item.save()
        
        for compet in Competition.objects.all():
            edicompet = EditionCompetition.objects.filter(competition = compet, is_finished = False).order_by("edition__name")
            if len(edicompet) > 1 :
                i = 0
                while i < len(edicompet)-1:
                    current_element = edicompet[i]
                    next_element = edicompet[i+1]
                    current_element.finish_date = next_element.start_date
                    current_element.is_finished = True
                    current_element.save()
                    i += 1
                  
    except Exception as e:
        print(e)
        