from django.core.management.base import BaseCommand, CommandError
import csv, os, re


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        contries = [x for x in os.listdir("datas/lot1/") if os.path.isdir("datas/lot1/{}".format(x))]
        
        year = 2013
        files = [x for x in os.listdir("datas/lot1/belgium") if not os.path.isdir("datas/lot1/belgium/{}".format(x))]
        for file in files:
            nb = re.findall('\d+', file)
            if len(nb) == 1:
                edition = "{}-{}".format(year, year+1)
            else:
                edition = "{}-{}".format(year-int(nb[-1]), year-int(nb[-1])+1)
            path = "datas/lot1/belgium/{}".format(edition)
            os.makedirs(path, exist_ok=True)
            os.rename("datas/lot1/belgium/{}".format(file), "datas/lot1/belgium/{}/{}".format(edition, "Jupyter league.csv"))
            print(edition)


        #     file.n
        # os.makedirs()
        # print(files)
        
        # with open('X:\data.csv','rt')as f:
        #     data = csv.reader(f)
        #     for row in data:
        #         print(row)

        self.stdout.write(self.style.SUCCESS('hello world !'))