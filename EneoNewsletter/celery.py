import os
import ssl

from celery import Celery
from django.conf import settings

# Définir le module de paramètres par défaut pour l'application Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EneoNewsletter.settings')

app = Celery('EneoNewsletter')

# Utiliser une chaîne de configuration pour que les tâches puissent être
# sérialisées en JSON
app.config_from_object('django.conf:settings', namespace='CELERY')

# Configuration du broker et du backend de résultat
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND

if settings.CELERY_BROKER_URL.startswith("rediss://"):
    app.conf.broker_use_ssl = {
        'ssl_cert_reqs': ssl.CERT_OPTIONAL
    }

# Configuration de la sérialisation
app.conf.accept_content = ['json']
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.timezone = settings.TIME_ZONE

# Charger automatiquement les tâches depuis toutes les applications Django
app.autodiscover_tasks()

# Forcer la découverte des tâches de l'application newsletter
app.autodiscover_tasks(['newsletter', 'coupure'])

# Cette tâche est utilisée pour tester que Celery fonctionne correctement
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
