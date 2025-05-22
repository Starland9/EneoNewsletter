from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('', views.home, name='home'),
    path('s\'inscrire/', views.subscribe, name='subscribe'),
    path('se-desabonner/', views.unsubscribe, name='unsubscribe'),
    path('se-desabonner/<str:token>/', views.unsubscribe, name='unsubscribe_with_token'),
    path('archives/', views.newsletter_list, name='list'),
    path('archives/<int:pk>/', views.newsletter_detail, name='detail'),
]
