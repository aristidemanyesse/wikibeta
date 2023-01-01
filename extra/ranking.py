from competitionApp.models import *
from datetime import datetime

def function():
    print("-------------------------", datetime.now())
    
    for edition in EditionCompetition.objects.all():
        if edition.edition_rankings.all().count() > 0 and edition.is_finished:
            continue
        
        
        print("Ranking de --", edition)
        datas = edition.classement()
        
        rank = Ranking.objects.create(
            edition = edition,
        )
        
        for line in datas:
            LigneRanking.objects.create(
                ranking = rank,
                team =  line["team"],
                mj   =  line["mj"],
                win  =  line["win"],
                draw =  line["draw"],
                lose =  line["lose"],
                gs   =  line["gs"],
                ga   =  line["ga"],
                gd   =  line["gd"],
                form  =  line["form"],
                pts  =  line["pts"],
                ppg  =  line["ppg"],
                cs   =  line["cs"],
                btts =  line["btts"],
                avg_gs = line["avg_gs"],
                p1_5 =  line["p1_5"],
                p2_5 =  line["p2_5"],
                m3_5 =  line["m3_5"],
            )
