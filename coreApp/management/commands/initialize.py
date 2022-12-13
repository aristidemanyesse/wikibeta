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
        
                               
            for x in os.listdir("datas/lot/"):
                if os.path.isdir("datas/lot/{}".format(x)) : 
                    files = [file for file in os.listdir("datas/lot/{}".format(x)) if not os.path.isdir("datas/lot/{}/{}".format(x, file))]
                    for file in files:
                        if threading.active_count() > 145:
                            time.sleep(360)
                        print("START: Current active thread count ---------------: ", threading.active_count())
                        path = "datas/lot/{}/{}".format(x, file)
                        p = threading.Thread(target=save_from_dir , args=(path,))
                        p.setDaemon(True)
                        p.start()
                        time.sleep(1)

                else:
                    if threading.active_count() > 145:
                        time.sleep(360)
                    print("START: Current active thread count ---------------: ", threading.active_count())
                    path = "datas/lot/{}".format(x)
                    p = threading.Thread(target=save_from_file , args=(path,))
                    p.setDaemon(True)
                    p.start()
                    time.sleep(1)
                    
                    
            self.stdout.write(self.style.SUCCESS('Base de données initialisée avec succes !'))
            
        except Exception as e:
            print(e)
