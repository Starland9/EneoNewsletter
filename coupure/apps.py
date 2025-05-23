from django.apps import AppConfig


class CoupureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coupure'
    verbose_name = 'Gestion des coupures'
    
    def ready(self):
        # Importer les signaux pour s'assurer qu'ils sont enregistrés
        import coupure.signals  # noqa
