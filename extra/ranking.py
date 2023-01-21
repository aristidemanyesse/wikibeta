from competitionApp.models import *
from datetime import datetime, timedelta

def function():
    print("-------------------------", datetime.now())
    
    try :
        for edition in EditionCompetition.objects.all(is_finished = False):
            last = edition.edition_rankings.all().first()
            
            if last in None or last.created_at > datetime.now() - timedelta(days=3):
                print("Ranking de --", edition)
                datas = edition.classement()
                print(datas)
                
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
    except Exception as e:
        print("Error ", e)
