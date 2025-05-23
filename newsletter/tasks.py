from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from .models import Newsletter, Subscriber
from django.utils import timezone


@shared_task(bind=True, max_retries=3)
def send_newsletter_task(self, newsletter_id, request_domain):
    """
    Tâche asynchrone pour envoyer une newsletter à tous les abonnés actifs
    """
    try:
        newsletter = Newsletter.objects.get(id=newsletter_id)
        
        # Mettre à jour le statut de la newsletter
        newsletter.status = Newsletter.STATUS_SENDING
        newsletter.save()
        
        # Récupérer tous les abonnés actifs
        subscribers = Subscriber.objects.filter(is_active=True)
        
        total_recipients = subscribers.count()
        success_count = 0
        error_count = 0
        
        for subscriber in subscribers:
            try:
                # Construire l'URL de désinscription
                unsubscribe_url = f"https://{request_domain}{reverse('newsletter:unsubscribe_with_token', args=[subscriber.token])}"
                
                # Rendre le contenu HTML du mail
                html_message = render_to_string('newsletter/emails/newsletter_email.html', {
                    'newsletter': newsletter,
                    'subscriber': subscriber,
                    'unsubscribe_url': unsubscribe_url,
                    'site_url': f'https://{request_domain}'
                })
                
                # Créer une version texte du message
                plain_message = strip_tags(html_message)
                
                # Envoyer l'email
                send_mail(
                    subject=newsletter.subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                success_count += 1
                
            except Exception as e:
                error_count += 1
                # En cas d'erreur, réessayer la tâche après un délai
                self.retry(exc=e, countdown=60 * 5)  # Réessayer après 5 minutes
        
        # Mettre à jour le statut de la newsletter
        newsletter.status = Newsletter.STATUS_SENT
        newsletter.sent_at = timezone.now()
        newsletter.save()
        
        return {
            'status': 'completed',
            'total_recipients': total_recipients,
            'success_count': success_count,
            'error_count': error_count
        }
        
    except Exception as e:
        # En cas d'erreur critique, mettre à jour le statut de la newsletter
        newsletter.status = Newsletter.STATUS_DRAFT
        newsletter.save()
        raise self.retry(exc=e, countdown=60 * 5)  # Réessayer après 5 minutes
