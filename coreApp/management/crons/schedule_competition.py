from competitionApp.models import *
import datetime

def handle():
    try:   
        print("--------------------------------", datetime.datetime.now()) 
        for item in EditionCompetition.objects.filter(is_finished = False).exclude(start_date = None).order_by("edition__name"):
            matchs = item.edition_du_match.filter(deleted = False).exclude(date = None).order_by("date")
            match = matchs.first()
            if  match is not None:
                item.start_date = matchs.first().date
                item.finish_date = matchs.last().date
                item.save()
        
        for compet in Competition.objects.all():
            edicompet = EditionCompetition.objects.filter(competition = compet, is_finished = False).order_by("edition__name")
            current_element = edicompet.first()
            if current_element is not None:
                if len(edicompet) > 1 :
                    matchs = current_element.edition_du_match.filter(deleted = False).order_by("date").exclude(date = None)
                    match = matchs.last()
                    current_element.finish_date = match.date
                else:
                    next_element = edicompet[1]
                    current_element.finish_date = next_element.start_date
                    current_element.is_finished = True
                current_element.save()
                  
    except Exception as e:
        print(e)
        