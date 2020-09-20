import django_filters
from django_filters import CharFilter
from django.forms import TextInput
from .models import Card, Profile
from django.contrib.auth.models import User

class CardFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains', label="", widget=TextInput(attrs={'placeholder': 'Search cards'}))
    class Meta:
        model = Card
        fields = ['name']


class UserFilter(django_filters.FilterSet):
    username = CharFilter(field_name='username', lookup_expr='icontains', label="", widget=TextInput(attrs={'placeholder': 'Search users'}))
    class Meta:
        model = User
        fields = ['username']
