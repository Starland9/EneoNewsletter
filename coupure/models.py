from django.db import models
from newsletter.models import Subscriber
from django.db.models import Q
from unidecode import unidecode

class Coupure(models.Model):
    observations = models.TextField(verbose_name="Observations")
    date = models.DateField(verbose_name="Date de la coupure")
    heure_debut = models.CharField(max_length=10, verbose_name="Heure de début")
    heure_fin = models.CharField(max_length=10, verbose_name="Heure de fin")
    region = models.CharField(max_length=100, verbose_name="Région")
    ville = models.CharField(max_length=100, verbose_name="Ville", blank=True)
    quartier = models.CharField(max_length=100, verbose_name="Quartier")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    subscribers_notified = models.ManyToManyField(
        Subscriber,
        related_name='coupures_notified',
        blank=True,
        verbose_name="Abonnés notifiés"
    )

    class Meta:
        verbose_name = "Coupure programmée"
        verbose_name_plural = "Coupures programmées"
        ordering = ['date', 'heure_debut']

    def __str__(self):
        return f"{self.quartier} - {self.date} ({self.heure_debut}-{self.heure_fin})"

    def get_affected_subscribers(self):
        """
        Retourne les abonnés concernés par cette coupure en effectuant une recherche
        souple sur le nom du quartier (insensible à la casse, aux accents et aux espaces).
        Gère les cas comme "BEPENDA OMNISPORT" et "Bepanda".
        """
        # Nettoyer et normaliser le quartier de la coupure
        quartier_coupure = unidecode(self.quartier.strip().lower())
        
        # Récupérer tous les abonnés actifs
        subscribers = Subscriber.objects.filter(is_active=True)
        
        # Liste pour stocker les abonnés correspondants
        matching_subscribers = []
        
        # Mots à ignorer dans la comparaison
        stop_words = {'le', 'la', 'les', 'de', 'des', 'du', 'et', 'à', 'en', 'sur', 'sous', 'dans'}
        
        # Nettoyer et séparer les mots du quartier de la coupure
        def clean_quartier(quartier):
            # Supprimer la ponctuation et les chiffres
            import re
            quartier = re.sub(r'[^\w\s]', ' ', quartier)
            # Remplacer les espaces multiples par un seul espace
            quartier = ' '.join(quartier.split())
            # Mettre en minuscule et supprimer les accents
            quartier = unidecode(quartier.lower())
            # Supprimer les mots vides
            mots = [mot for mot in quartier.split() if mot not in stop_words]
            return set(mots)
        
        mots_quartier_coupure = clean_quartier(quartier_coupure)
        
        for subscriber in subscribers:
            # Nettoyer et normaliser le quartier de l'abonné
            quartier_abonne = unidecode(subscriber.neighborhood.strip().lower())
            mots_quartier_abonne = clean_quartier(quartier_abonne)
            
            # Vérifier s'il y a une correspondance entre les mots
            mots_communs = mots_quartier_coupure.intersection(mots_quartier_abonne)
            
            # Si au moins un mot en commun ou si un quartier est contenu dans l'autre
            if (mots_communs or 
                any(mot in quartier_abonne for mot in mots_quartier_coupure) or
                any(mot in quartier_coupure for mot in mots_quartier_abonne) or
                quartier_abonne in quartier_coupure or 
                quartier_coupure in quartier_abonne):
                
                matching_subscribers.append(subscriber.id)
        
        # Retourner les abonnés correspondants
        return Subscriber.objects.filter(id__in=matching_subscribers)
