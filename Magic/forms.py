from django.contrib.auth.models import User
from Magic.models import Card, Profile, Address
from django import forms

'''
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
'''
class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ['user']

class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'apartment_number', 'country', 'zip_code']