from competitionApp.models import *

def handle():
    try:    
        for item in EditionCompetition.objects.all().order_by("edition__name"):
            matchs = item.edition_du_match.filter(deleted = False).order_by("date").exclude(date = None)
            if  matchs.first() is not None:
                item.start_date =   matchs.first().date   
                item.save()
        
        for pays in Pays.objects.all():
            edicompet = EditionCompetition.objects.filter(competition__pays = pays).order_by("edition__name")
            for i in range(len(edicompet) - 1):
                if i == (len(edicompet) - 1):
                    continue
                current_element = edicompet[i]
                next_element = edicompet[i + 1]
                
                current_element.finish_date = next_element.start_date
                current_element.is_finished = True
                current_element.save()
                  
    except Exception as e:
        print(e)
        