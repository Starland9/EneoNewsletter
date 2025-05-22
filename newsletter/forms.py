from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone
from .models import Subscriber, Newsletter
import uuid

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email', 'first_name', 'last_name']
        labels = {
            'email': 'Adresse email',
            'first_name': 'Prénom',
            'last_name': 'Nom',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Subscriber.objects.filter(email=email, is_active=True).exists():
            raise ValidationError('Cette adresse email est déjà inscrite à notre newsletter.')
        return email
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.token = str(uuid.uuid4())
        if commit:
            instance.save()
        return instance


class UnsubscribeForm(forms.Form):
    email = forms.EmailField(
        label='Votre adresse email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'})
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Subscriber.objects.filter(email=email, is_active=True).exists():
            raise ValidationError('Cette adresse email n\'est pas inscrite à notre newsletter.')
        return email


class NewsletterAdminForm(ModelForm):
    class Meta:
        model = Newsletter
        fields = ['subject', 'content', 'status']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'vTextField', 'size': '90'}),
            'content': forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 20, 'cols': 90}),
            'status': forms.Select(attrs={'class': 'vSelect'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        
        # Vérifier que le contenu n'est pas vide
        if not cleaned_data.get('content'):
            raise ValidationError({
                'content': 'Le contenu de la newsletter ne peut pas être vide.'
            })
        
        # Vérifier que le sujet n'est pas vide
        if not cleaned_data.get('subject'):
            raise ValidationError({
                'subject': 'Le sujet de la newsletter ne peut pas être vide.'
            })
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Ensure cleaned_data is populated
        if not hasattr(self, 'cleaned_data') or not self.cleaned_data:
            self.cleaned_data = self.cleaned_data or {}
            
        # Si c'est une nouvelle newsletter ou si le statut est modifié
        if not instance.pk or 'status' in self.changed_data:
            if self.cleaned_data.get('status') == Newsletter.STATUS_SENT:
                instance.sent_at = timezone.now()
        
        if commit:
            instance.save()
        
        return instance
