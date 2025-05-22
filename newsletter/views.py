from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Subscriber, Newsletter
from .forms import SubscribeForm, UnsubscribeForm
import uuid


def home(request):
    return render(request, 'newsletter/home.html')


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            
            # Envoyer un email de confirmation
            subject = 'Confirmation de votre inscription à notre newsletter'
            html_message = render_to_string('newsletter/emails/welcome_email.html', {
                'subscriber': subscriber,
                'unsubscribe_url': request.build_absolute_uri(f'/newsletter/unsubscribe/{subscriber.token}/')
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Merci pour votre inscription ! Un email de confirmation vous a été envoyé.')
            return redirect('newsletter:home')
    else:
        form = SubscribeForm()
    
    return render(request, 'newsletter/subscribe.html', {'form': form})


def unsubscribe(request, token=None):
    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                subscriber = Subscriber.objects.get(email=email, is_active=True)
                subscriber.is_active = False
                subscriber.unsubscribed_date = timezone.now()
                subscriber.save()
                messages.success(request, 'Vous avez été désabonné de notre newsletter avec succès.')
                return redirect('newsletter:home')
            except Subscriber.DoesNotExist:
                messages.error(request, 'Cette adresse email n\'est pas inscrite à notre newsletter.')
    else:
        form = UnsubscribeForm()
        
        # Si un token est fourni, pré-remplir le formulaire avec l'email correspondant
        if token:
            try:
                subscriber = Subscriber.objects.get(token=token, is_active=True)
                form = UnsubscribeForm(initial={'email': subscriber.email})
            except Subscriber.DoesNotExist:
                messages.error(request, 'Lien de désinscription invalide ou expiré.')
    
    return render(request, 'newsletter/unsubscribe.html', {'form': form})


def newsletter_list(request):
    newsletters = Newsletter.objects.filter(status=Newsletter.STATUS_SENT).order_by('-sent_at')
    return render(request, 'newsletter/list.html', {'newsletters': newsletters})


def newsletter_detail(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk, status=Newsletter.STATUS_SENT)
    return render(request, 'newsletter/detail.html', {'newsletter': newsletter})
