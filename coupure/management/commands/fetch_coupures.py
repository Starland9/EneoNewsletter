from django.core.management.base import BaseCommand
from coupure.tasks import fetch_and_notify_coupures

class Command(BaseCommand):
    help = 'Récupère les dernières coupures programmées depuis l\'API Eneo et envoie des notifications aux abonnés concernés'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Démarrage de la récupération des coupures...'))
        
        try:
            # Lancer la tâche asynchrone
            result = fetch_and_notify_coupures.delay()
            
            self.stdout.write(
                self.style.SUCCESS(f'Récupération des coupures lancée avec succès (ID de tâche: {result.id})')
            )
            self.stdout.write(
                self.style.WARNING('Remarque: L\'envoi des notifications se fera en arrière-plan.')
            )
            
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f'Erreur lors du lancement de la tâche: {str(e)}')
            )
