from django.core.management.base import BaseCommand, CommandError
import csv, os, re


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        contries = [x for x in os.listdir("datas/lot1/") if os.path.isdir("datas/lot1/{}".format(x))]
        
        year = 2013
        files = [x for x in os.listdir("datas/lot1/france") if not os.path.isdir("datas/lot1/france/{}".format(x))]
        for file in files:
            nb = re.findall('\d+', file)
            if nb[0] == "1":
                if len(nb) == 1:
                    edition = "{}-{}".format(year, year+1)
                else:
                    edition = "{}-{}".format(year-int(nb[-1]), year-int(nb[-1])+1)
                path = "datas/lot1/france/{}".format(edition)
                os.makedirs(path, exist_ok=True)
                os.rename("datas/lot1/france/{}".format(file), "datas/lot1/france/{}/{}".format(edition, "Ligue 1.csv"))
                print(edition)


        #     file.n
        # os.makedirs()
        # print(files)
        
        # with open('X:\data.csv','rt')as f:
        #     data = csv.reader(f)
        #     for row in data:
        #         print(row)

        self.stdout.write(self.style.SUCCESS('hello world !'))