from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from competitionApp.models import *


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        print("-------------------------", datetime.now())
    
        try :
            for edition in EditionCompetition.objects.all(is_finished = False):
                last = edition.edition_rankings.all().first()
                
                if last in None or last.created_at > datetime.now() - timedelta(days=2):
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
                    
                    # total = 0
                    # for ligne in rank.ranking_lignes.all():
                    #     ppg += ligne.ppg
                    #     avg_gs += ligne.avg_gs
                    #     ppg += ligne.ppg
                    #     ppg += ligne.ppg
                    #     ppg += ligne.ppg
                        
                    # CompetitionStat.objects.create(
                    #     edition             = edition,
                    #     ranking             = rank,
                    #     ppg                 = total += x.ppg for x in lignes
                    #     avg_goals    = models.FloatField(null = True, blank=True)
                    #     avg_fouls           = models.FloatField(null = True, blank=True)
                    #     avg_corners         = models.FloatField(null = True, blank=True)
                    #     avg_shots           = models.FloatField(null = True, blank=True)
                    #     avg_shots_target    = models.FloatField(null = True, blank=True)
                    #     avg_offside         = models.FloatField(null = True, blank=True)
                    #     avg_cards           = models.FloatField(null = True, blank=True)
                    # )

        except Exception as e:
            print("Error ", e)
