from django.contrib.auth.models import User
from Magic.models import Card, Profile, Address
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_COICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    fist_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Takács'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'László'
    }))
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Kossuth Lajos utca'
    }))
    apartment_number = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder':'35'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class':'custom-select d-block w-100'
    }))
    zip_code = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder':'1758',
    }))
    #payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_COICES)