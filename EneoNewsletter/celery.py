import os
from celery import Celery
from django.conf import settings

# Définir le module de paramètres par défaut pour l'application Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EneoNewsletter.settings')

app = Celery('EneoNewsletter')

# Utiliser une chaîne de configuration pour que les tâches puissent être
# sérialisées en JSON
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger automatiquement les tâches depuis toutes les applications Django
app.autodiscover_tasks()

# Forcer la découverte des tâches de l'application newsletter
app.autodiscover_tasks(['newsletter'])

# Cette tâche est utilisée pour tester que Celery fonctionne correctement
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
