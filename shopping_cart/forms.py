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
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'1234 Main st'
    }))
    apartment_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Apartment number'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class':'custom-select d-block w-100'
    }))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Zip code',
    }))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_COICES)