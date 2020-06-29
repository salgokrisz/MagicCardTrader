from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Magic Card Trader Home'),
    path('about/', views.about, name='Magic Card Trader About'),
]