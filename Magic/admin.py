from django.contrib import admin
from .models import Profile, Card, Address

#admin.site.register(User)
admin.site.register(Card)
admin.site.register(Profile)
admin.site.register(Address)

