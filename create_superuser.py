import os
import django
from django.contrib.auth import get_user_model
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EneoNewsletter.settings')
django.setup()


def create_superuser():
    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'changeme123')

    # Utilisation de call_command pour créer le superutilisateur
    call_command(
        'createsuperuser',
        '--noinput',
        '--username', username,
        '--email', email
    )

    # Mise à jour du mot de passe
    User = get_user_model()
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f"Superutilisateur {username} créé avec succès !")


if __name__ == '__main__':
    create_superuser()