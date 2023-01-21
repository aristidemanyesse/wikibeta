from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from competitionApp.models import *


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:     
    
            Ranking.objects.all().delete()

            for edition in EditionCompetition.objects.filter(is_finished = False):
                last = edition.edition_rankings.all().first()
                
                if last is None or last.created_at > datetime.now() - timedelta(days=3):
                    print("Ranking de --", edition)
                    datas = edition.classement()
                    
                    rank = Ranking.objects.create(
                        edition = edition,
                    )
                    
                    for i, line in enumerate(datas):
                        LigneRanking.objects.create(
                            ranking = rank,
                            level = i+1,
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
                            avg_ga = line["avg_ga"],
                            p1_5 =  line["p1_5"],
                            p2_5 =  line["p2_5"],
                            m3_5 =  line["m3_5"],
                        )
        except Exception as e:
            print("Error ", e)
