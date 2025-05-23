import requests
from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import Coupure

@shared_task(bind=True, max_retries=1)
def fetch_and_notify_coupures(self):
    """
    Tâche qui récupère les coupures depuis l'API Eneo et envoie des notifications
    aux abonnés concernés.
    """
    url = 'https://alert.eneo.cm/ajaxOutage.php'
    data = None

    for i in range(1, 11):
        try:
            # Récupérer les données des coupures
            response = requests.post(
                url,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json',
                },
                data={'region': i}
            )

            response.raise_for_status()
            data = response.json()

            if data.get('status') != 1:
                raise ValueError("Réponse inattendue de l'API Eneo")

            # Traiter chaque coupure
            for item in data.get('data', []):
                # Vérifier si cette coupure existe déjà
                if not Coupure.objects.filter(
                    date=item['prog_date'],
                    quartier__iexact=item['quartier'].strip(),
                    heure_debut=item['prog_heure_debut'],
                    heure_fin=item['prog_heure_fin']
                ).exists():
                    # Créer une nouvelle entrée de coupure
                    coupure = Coupure.objects.create(
                        observations=item['observations'],
                        date=item['prog_date'],
                        heure_debut=item['prog_heure_debut'],
                        heure_fin=item['prog_heure_fin'],
                        region=item['region'],
                        ville=item.get('ville', ''),
                        quartier=item['quartier'].strip(),

                    )

                    # Notifier les abonnés concernés
                    notify_subscribers_about_coupure.delay(coupure.id)

        except Exception as e:
            # En cas d'erreur, réessayer après un délai
            self.retry(exc=e, countdown=60)  # Réessayer après 5 minutes

    if data:
        return {
            'status': 'success',
            'message': f"{len(data.get('data', []))} coupures traitées"
        }
    else:
        return {
            'status': 'error',
            'message': 'Aucune données récupérées'
        }


@shared_task
def notify_subscribers_about_coupure(coupure_id):
    """
    Envoie des notifications aux abonnés concernés par une coupure
    """
    try:
        coupure = Coupure.objects.get(id=coupure_id)
        subscribers = coupure.get_affected_subscribers()
        
        if not subscribers.exists():
            return {'status': 'no_subscribers', 'count': 0}
        
        count = 0
        for subscriber in subscribers:
            try:
                # Construire le contenu de l'email
                subject = f"Coupure programmée dans votre quartier - {coupure.quartier}"
                context = {
                    'coupure': coupure,
                    'subscriber': subscriber,
                    'unsubscribe_url': f"https://{settings.DOMAIN}/newsletter/unsubscribe/{subscriber.token}/"
                }
                
                html_message = render_to_string('coupure/emails/coupure_notification.html', context)
                plain_message = render_to_string('coupure/emails/coupure_notification.txt', context)
                
                # Envoyer l'email
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                # Marquer l'abonné comme notifié
                coupure.subscribers_notified.add(subscriber)
                count += 1
                
            except Exception as e:
                # Continuer avec les autres abonnés en cas d'erreur
                print(f"Erreur lors de l'envoi à {subscriber.email}: {str(e)}")
        
        return {'status': 'success', 'count': count}
        
    except Coupure.DoesNotExist:
        return {'status': 'error', 'message': 'Coupure non trouvée'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
