from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Coupure
from .tasks import fetch_and_notify_coupures


@admin.register(Coupure)
class CoupureAdmin(admin.ModelAdmin):
    list_display = ('quartier', 'date', 'heure_debut', 'heure_fin', 'region')
    list_filter = ('date', 'region', 'ville')
    search_fields = ('quartier', 'ville', 'region', 'observations')
    readonly_fields = ('created_at', 'updated_at', 'notified_subscribers_list')
    date_hierarchy = 'date'
    actions = ['fetch_coupures_action', 'resend_notifications']
    
    fieldsets = (
        ('Informations de la coupure', {
            'fields': (
                'observations',
                ('date', 'heure_debut', 'heure_fin'),
                ('region', 'ville', 'quartier'),
            )
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at', 'subscribers_notified'),
            'classes': ('collapse',),
        }),
    )

    # @admin.display(description='Abonnés notifiés')
    # def get_notified_subscribers_count(self, obj):
    #     return obj.subscribers_notified.count()

    def notified_subscribers_list(self, obj):
        subscribers = obj.subscribers_notified.all()
        if not subscribers:
            return "Aucun abonné notifié"
        
        links = []
        for subscriber in subscribers:
            url = reverse('admin:newsletter_subscriber_change', args=[subscriber.id])
            links.append(f'<a href="{url}">{subscriber.email}</a>')
        
        return mark_safe('<br>'.join(links))
    notified_subscribers_list.short_description = 'Abonnés notifiés'
    notified_subscribers_list.allow_tags = True
    
    def fetch_coupures_action(self, request, queryset):
        """Action pour récupérer les dernières coupures depuis l'API Eneo"""
        result = fetch_and_notify_coupures.delay()
        self.message_user(
            request,
            f"La récupération des coupures a été lancée en arrière-plan (ID: {result.id})"
        )
    fetch_coupures_action.short_description = "Récupérer les dernières coupures"
    
    def resend_notifications(self, request, queryset):
        """Action pour renvoyer les notifications pour les coupures sélectionnées"""
        from .tasks import notify_subscribers_about_coupure
        count = 0
        for coupure in queryset:
            notify_subscribers_about_coupure.delay(coupure.id)
            count += 1
        self.message_user(
            request,
            f"Les notifications pour {count} coupure(s) seront envoyées en arrière-plan"
        )
    resend_notifications.short_description = "Renvoyer les notifications"
