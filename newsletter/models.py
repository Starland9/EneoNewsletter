from django.db import models
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class Subscriber(models.Model):
    email = models.EmailField(unique=True, validators=[validate_email])
    first_name = models.CharField(max_length=100, blank=True, verbose_name='Prénom')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='Nom')
    neighborhood = models.CharField(max_length=100, blank=True, verbose_name='Quartier')
    is_active = models.BooleanField(default=True, verbose_name='Actif')
    subscribed_date = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    unsubscribed_date = models.DateTimeField(null=True, blank=True, verbose_name='Date de désinscription')
    token = models.CharField(max_length=100, unique=True, blank=True, verbose_name='Jeton de sécurité')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Abonné'
        verbose_name_plural = 'Abonnés'
        ordering = ['-subscribed_date']


class Newsletter(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_SENDING = 'sending'
    STATUS_SENT = 'sent'
    
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Brouillon'),
        (STATUS_SENDING, 'Envoi en cours'),
        (STATUS_SENT, 'Envoyé'),
    ]
    
    subject = models.CharField(max_length=200, verbose_name='Sujet')
    content = models.TextField(verbose_name='Contenu')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=STATUS_DRAFT,
        verbose_name='Statut'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Dernière modification')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Date d'envoi")
    
    def __str__(self):
        return self.subject
    
    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'
        ordering = ['-created_at']
