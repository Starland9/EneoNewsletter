from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.shortcuts import render
from .models import Subscriber, Newsletter
from .forms import NewsletterAdminForm
from .tasks import send_newsletter_task
from django.contrib import messages


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'subscribed_date', 'unsubscribed_date')
    list_filter = ('is_active', 'subscribed_date', 'unsubscribed_date')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('subscribed_date', 'unsubscribed_date', 'token')
    list_per_page = 20
    actions = ['export_emails', 'send_test_newsletter']
    
    def export_emails(self, request, queryset):
        emails = queryset.values_list('email', flat=True)
        response = HttpResponse("\n".join(emails), content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=subscribers_emails.txt'
        return response
    export_emails.short_description = "Exporter les emails sélectionnés"
    
    def send_test_newsletter(self, request, queryset):
        if request.method == 'POST' and '_send' in request.POST:
            newsletter_id = request.POST.get('newsletter')
            if not newsletter_id:
                self.message_user(request, 'Veuillez sélectionner une newsletter.', level='error')
                return None

            try:
                newsletter = Newsletter.objects.get(id=newsletter_id)
                sent_count = 0
                error_count = 0

                for subscriber in queryset:
                    try:
                        # Build the unsubscribed URL with the token
                        unsubscribe_url = request.build_absolute_uri(
                            reverse('newsletter:unsubscribe_with_token', args=[subscriber.token])
                        )

                        # Render email content
                        html_message = render_to_string('newsletter/emails/newsletter_email.html', {
                            'newsletter': newsletter,
                            'subscriber': subscriber,
                            'unsubscribe_url': unsubscribe_url,
                            'site_url': request.build_absolute_uri('/')
                        })
                        plain_message = strip_tags(html_message)

                        # Send email
                        send_mail(
                            subject=f"[TEST] {newsletter.subject}",
                            message=plain_message,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[subscriber.email],
                            html_message=html_message,
                            fail_silently=False,
                        )
                        sent_count += 1

                    except Exception as e:
                        error_count += 1
                        # Log the error but continue with other subscribers
                        self.message_user(
                            request,
                            f'Erreur lors de l\'envoi à {subscriber.email}: {str(e)}',
                            level='error'
                        )

                # Show a success message with stats
                if sent_count > 0:
                    self.message_user(
                        request,
                        f'Newsletter de test envoyée avec succès à {sent_count} abonné(s).',
                        level='success'
                    )
                if error_count > 0:
                    self.message_user(
                        request,
                        f'Des erreurs sont survenues lors de l\'envoi à {error_count} abonné(s).',
                        level='warning'
                    )

                # Redirect to prevent form resubmission
                return None

            except Newsletter.DoesNotExist:
                self.message_user(request, 'La newsletter sélectionnée n\'existe pas.', level='error')
            except Exception as e:
                self.message_user(
                    request,
                    f'Une erreur est survenue : {str(e)}',
                    level='error'
                )

        # Display the newsletter selection form
        newsletters = Newsletter.objects.all()
        context = {
            'title': 'Envoyer une newsletter de test',
            'subscribers': queryset,
            'newsletters': newsletters,
            'opts': self.model._meta,
            'media': self.media,
        }
        return render(request, 'admin/send_test_newsletter.html', context=context)
    send_test_newsletter.short_description = "Envoyer une newsletter de test"


class NewsletterAdmin(admin.ModelAdmin):
    form = NewsletterAdminForm
    list_display = ('subject', 'status', 'created_at', 'sent_at', 'preview_link')
    list_filter = ('status', 'created_at', 'sent_at')
    search_fields = ('subject', 'content')
    readonly_fields = ('created_at', 'updated_at', 'sent_at', 'status')
    actions = ['send_newsletter']
    
    def preview_link(self, obj):
        if obj.status == Newsletter.STATUS_SENT:
            return format_html(
                '<a href="{}" target="_blank">Aperçu</a>',
                reverse('newsletter:detail', args=[obj.pk])
            )
        return "-"
    preview_link.short_description = "Aperçu"
    
    def save_model(self, request, obj, form, change):
        # Si on clique sur le bouton "Envoyer la newsletter"
        if 'send_newsletter' in request.POST and obj.status == Newsletter.STATUS_DRAFT:
            # Sauvegarder d'abord l'objet pour obtenir un ID
            super().save_model(request, obj, form, change)
            
            # Obtenir le domaine pour construire les URLs absolues
            domain = request.get_host()
            
            # Lancer la tâche asynchrone
            send_newsletter_task.delay(obj.id, domain)
            
            # Afficher un message à l'utilisateur
            from django.contrib import messages
            messages.success(
                request,
                'L\'envoi de la newsletter a commencé. Vous serez notifié une fois terminé.'
            )
        else:
            # Sauvegarder normalement sans envoyer
            super().save_model(request, obj, form, change)
    
    def send_newsletter(self, request, queryset):

        
        domain = request.get_host()
        count = 0
        
        for newsletter in queryset:
            if newsletter.status == Newsletter.STATUS_DRAFT:
                # Marquer comme en cours d'envoi
                newsletter.status = Newsletter.STATUS_SENDING
                newsletter.save()
                
                # Lancer la tâche asynchrone
                send_newsletter_task.delay(newsletter.id, domain)
                count += 1
        
        if count > 0:
            messages.success(
                request,
                f"L'envoi de {count} newsletter(s) a commencé. "
                "Vous serez notifié une fois terminé."
            )
        else:
            messages.warning(request, "Aucune newsletter en brouillon sélectionnée.")
    send_newsletter.short_description = "Envoyer la newsletter"


admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
