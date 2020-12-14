from django.contrib.auth.models import User
from Magic.models import Card, Profile, Address
from django import forms
from mtgsdk import Card as MtgCard
from mtgsdk import Set as MtgSet

# form for card add and update
# defining the fields of the form
class CardForm(forms.ModelForm):
    
    class Meta:
        model = Card
        fields = ['name', 'set_name', 'price', 'is_foil']
        widgets = {
            'image_url': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'placeholder':'e.g. Rhystic Study'}),
            'set_name': forms.TextInput(attrs={'placeholder':'e.g. Prophecy'}),
            'price': forms.NumberInput(attrs={'placeholder':'Ft'}),
        }

# address form
# defining the fields
class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'apartment_number', 'country', 'zip_code']
