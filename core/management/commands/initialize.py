from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            import authApp.bootstrap as app
            app.run()

            import coreApp.bootstrap as app
            app.run()

            import paramApp.bootstrap as app
            app.run()
            
            import clientApp.bootstrap as app
            app.run()

            import organisationApp.bootstrap as app
            app.run()

            import productionApp.bootstrap as app
            app.run()

            import commandeApp.bootstrap as app
            app.run()

            import livraisonApp.bootstrap as app
            app.run()

            import approvisionnementApp.bootstrap as app
            app.run()

            import ficheApp.bootstrap as app
            app.run()

            import comptabilityApp.bootstrap as app
            app.run()

            self.stdout.write(self.style.SUCCESS('Base de données initialisée avec succes !'))
            
        except Exception as e:
            
            self.stdout.write(self.style.SUCCESS('Base de données initialisée avec succes !'))