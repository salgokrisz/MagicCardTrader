from django.db import models
from django.contrib.auth.models import User
from Magic.models import Card, Profile, Address


class OrderItem(models.Model):
    card = models.OneToOneField(Card, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return "{}".format(self.card)

class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return round(sum([item.card.price for item in self.items.all()]), 2)

    def __str__(self):
        return "{} - {}".format(self.owner, self.ref_code)


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.stripe_charge_id

    class Meta:
        ordering = ['-timestamp']
