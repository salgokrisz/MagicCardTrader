from django.contrib.auth.models import User
from Magic.models import Card, Profile, Address
from django import forms
from mtgsdk import Card as MtgCard
from mtgsdk import Set as MtgSet

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
        fields = ['name', 'set_name', 'price', 'is_foil']
        widgets = {'image_url': forms.HiddenInput()}


class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'apartment_number', 'country', 'zip_code']
