from competitionApp.models import *
from coreApp.templatetags import footstats
from predictionApp.models import *


def prediction(match):
    
    try:
        if len( match.away.get_last_matchs(match, edition = True)) < 4 or len( match.home.get_last_matchs(match, edition = True)) < 4:
            return
        
        home_rank = LigneRanking.objects.filter(team = match.home, ranking__date__lte = match.date).order_by('-ranking__date').first()
        away_rank = LigneRanking.objects.filter(team = match.away, ranking__date__lte = match.date).order_by('-ranking__date').first()
        
        home_last_matchs = match.home.get_last_matchs(match, number = 10, edition = True)
        away_last_matchs = match.away.get_last_matchs(match, number = 10, edition = True)
        
        home_stats = match.get_home_before_stats()
        away_stats = match.get_away_before_stats()
        
        home_maitrise = match.home.maitrise(match)
        away_maitrise = match.away.maitrise(match)
        
        if home_stats is None or away_stats is None:
            return
                
        

        if not(home_stats.avg_corners_for == 0 and away_stats.avg_corners_against == 0):
            p = footstats.plus_but(home_last_matchs, 2.5) + footstats.plus_but(away_last_matchs, 2.5)
            m = footstats.moins_but(home_last_matchs, 2.5) + footstats.moins_but(away_last_matchs, 2.5)
            p4 = footstats.plus_but(home_last_matchs, 3.5) + footstats.plus_but(away_last_matchs, 3.5)
        
            total_home = home_stats.avg_corners_for + home_stats.avg_corners_against
            avg_home = total_home / 2
            total_away = away_stats.avg_corners_for + away_stats.avg_corners_against
            avg_away = total_away / 2

            ############################################################################################################################
            # MOINS DE 12.5 CORNERS DANS LE MATCH
            ############################################################################################################################
            if avg_home + avg_away < 9 and not(home_maitrise < 6 and away_maitrise < 6):
                Prediction.objects.create(
                    mode = ModePrediction.get("M4"),
                    type = TypePrediction.get("corner_m12_5"),
                    match = match,
                    pct = 85
                )

                
            ############################################################################################################################
            # PLUS DE 7.5 CORNERS DANS LE MATCH
            ############################################################################################################################  
            test = False                 
            if  avg_home + avg_away > 12 and total_home >= 11 and total_away >= 11:
                test = [a for a in [home_stats.avg_corners_for, home_stats.avg_corners_against, away_stats.avg_corners_for, away_stats.avg_corners_against] if a >= 3.5 ]
                if len(test) == 4:
                    test = True
                    
            if (p > m+1) and (home_rank.avg_gs + away_rank.avg_gs) >= 2.8  and p4 > 2:
                test = [a for a in [home_stats.avg_corners_for, home_stats.avg_corners_against, away_stats.avg_corners_for, away_stats.avg_corners_against] if a >= 3.5 ]
                if len(test) == 4:
                    test = True
                    
            if test:    
                Prediction.objects.create(
                    mode = ModePrediction.get("M4"),
                    type = TypePrediction.get("corner_p6_5"),
                    match = match,
                    pct = 85
                )
            
        
            
            
            total_home = home_stats.avg_fouls_for + home_stats.avg_fouls_against
            avg_home = total_home / 2
            total_away = away_stats.avg_fouls_for + away_stats.avg_fouls_against
            avg_away = total_away / 2
            # ############################################################################################################################
            # # FAUTES DANS LE MATCH
            # ############################################################################################################################
            if abs(total_home - total_away) < 4:                      
                if  0 < (total_home + total_away) / 2 < 25 :
                    Prediction.objects.create(
                        mode = ModePrediction.get("M4"),
                        type = TypePrediction.get("foul_m30_5"),
                        match = match,
                        pct = 85
                    )
                                        
                elif  26 <= (total_home + total_away) / 2 < 50 and not(home_maitrise < 6 and away_maitrise < 6) :
                    Prediction.objects.create(
                        mode = ModePrediction.get("M4"),
                        type = TypePrediction.get("foul_p20_5"),
                        match = match,
                        pct = 85
                )
        

            
        
            total_home = home_stats.avg_shots_target_for + home_stats.avg_shots_target_against
            avg_home = total_home / 2
            total_away = away_stats.avg_shots_target_for + away_stats.avg_shots_target_against
            avg_away = total_away / 2
            # ############################################################################################################################
            # # TIRS CADREES DANS LE MATCH
            # ############################################################################################################################  
            if abs(total_home - total_away) < 3:                                      
                if  (total_home + total_away) / 2 > 10 :
                    Prediction.objects.create(
                        mode = ModePrediction.get("M4"),
                        type = TypePrediction.get("shoot_target_p6_5"),
                        match = match,
                        pct = 85
                    )
                    
                elif  (total_home + total_away) / 2 < 8 :
                    Prediction.objects.create(
                        mode = ModePrediction.get("M4"),
                        type = TypePrediction.get("shoot_target_m11_5"),
                        match = match,
                        pct = 85
                    )
            
            
        
            total_home = home_stats.avg_shots_for + home_stats.avg_shots_against
            avg_home = total_home / 2
            total_away = away_stats.avg_shots_for + away_stats.avg_shots_against
            avg_away = total_away / 2
            # ############################################################################################################################
            # # TIRS  DANS LE MATCH
            # ############################################################################################################################  
            if abs(total_home - total_away) < 4:                
                if  0 < (total_home + total_away) / 2 < 27 :
                    Prediction.objects.create(
                        mode = ModePrediction.get("M4"),
                        type = TypePrediction.get("shoot_m30_5"),
                        match = match,
                        pct = 85
                    )
                                  
                elif  24 <= (total_home + total_away) / 2 < 50 :
                    Prediction.objects.create(
                        mode = ModePrediction.get("M4"),
                        type = TypePrediction.get("shoot_p20_5"),
                        match = match,
                        pct = 85
                    )
            
            
            
            
            total_home = home_stats.avg_cards_for + home_stats.avg_cards_against
            avg_home = total_home / 2
            total_away = away_stats.avg_cards_for + away_stats.avg_cards_against
            avg_away = total_away / 2
            # ############################################################################################################################
            # # TIRS CADREES DANS LE MATCH
            # ############################################################################################################################  
            if abs(total_home - total_away) <= 2:                    
                if  (total_home + total_away) / 2 > 4 and (home_maitrise < 6 and away_maitrise < 6):
                    Prediction.objects.create(
                        mode = ModePrediction.get("M4"),
                        type = TypePrediction.get("card_p2_5"),
                        match = match,
                        pct = 85
                    )
                    


    except Exception as e:
        print(e)

