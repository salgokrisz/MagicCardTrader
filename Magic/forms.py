from django.contrib.auth.models import User
from Magic.models import Card 
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ['user']