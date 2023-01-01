from django.core.management.base import BaseCommand, CommandError
import os, time
from settings import settings
from .extract_data import save_from_dir, save_from_file
from bettingApp.models import Bookmaker

import threading
    
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:       
            
            # FOR ALL BOOKMAKERS ##
            with open("datas/bookmakers.txt",'rt', encoding='utf-8' ) as file:
                for line in file:
                    code, name = line.split(" = ")
                    name = name.replace("home win odds", "").replace("draw odds", "").replace("away win odds", "")
                    #enregistrement des editions
                    booker, created = Bookmaker.objects.get_or_create(name = name.capitalize(), code = code[:-1])
        
                      
            list_files = os.listdir("datas/lot/")
            list_files = sorted(list_files)         
            for x in list_files:
                if os.path.isdir("datas/lot/{}".format(x)) : 
                    files = [file for file in os.listdir("datas/lot/{}".format(x)) if not os.path.isdir("datas/lot/{}/{}".format(x, file))]
                    for file in files:
                        print("processus en cours ---------------: ", threading.active_count())
                        while threading.active_count() >= 145:
                            time.sleep(100)
                        path = "datas/lot/{}/{}".format(x, file)
                        p = threading.Thread(target=save_from_dir , args=(path,))
                        p.setDaemon(True)
                        p.start()
                        time.sleep(1)

                else:
                    print("processus en cours ---------------: ", threading.active_count())
                    while threading.active_count() >= 145:
                        time.sleep(100)
                    path = "datas/lot/{}".format(x)
                    p = threading.Thread(target=save_from_file , args=(path,))
                    p.setDaemon(True)
                    p.start()
                    time.sleep(1)
                    

            while threading.active_count() > 0:
                print("en attente ---------------: ", threading.active_count())
                time.sleep(30)
            self.stdout.write(self.style.SUCCESS('List des matchs initialisée avec succes !'))
            
        except Exception as e:
            print(e)
