from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Coupure
from .tasks import notify_subscribers_about_coupure

@receiver(post_save, sender=Coupure)
def notify_subscribers_on_coupure_creation(sender, instance, created, **kwargs):
    """
    Déclenche l'envoi de notifications lorsqu'une nouvelle coupure est créée
    """
    if created:
        # Lancer la tâche d'envoi de notifications de manière asynchrone
        notify_subscribers_about_coupure.delay(instance.id)
