from django.db import models
from django.db.models import Count
from django.urls import reverse
from mtgsdk import Card


class User(models.Model):
    name = models.CharField(max_length = 250)
    email_address = models.CharField(max_length = 500)
    #available_cards = models.IntegerField()
    user_photo = models.FileField(upload_to='profile_images', default='profile_images/Magic_card_back.jpg')


    def __str__ (self):
        return self.name# + " - Cards for sale: " + str(self.available_cards)#str(Card.objects.annotate(total=Count('user')))



def get_image_url(name, set_name):
        listOfVersions = []
        versions = Card.where(name=name, set=set_name).all()
        for card in versions:
            listOfVersions.append(card.image_url)
        listOfVersions = list(dict.fromkeys(listOfVersions))
        print(listOfVersions)
        return listOfVersions

class Card(models.Model):
    name = models.CharField(max_length = 150)
    set_name = models.CharField(max_length = 150)
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_foil = models.BooleanField(default=False)
    imageUrl = models.TextField(default=get_image_url(name, set_name))


    def get_absolute_url(self):
        return reverse('Magic:user_detail', kwargs={'user_id': self.user.id})

    @classmethod
    def user_cards(self):
        return Card.objects.annotate(total=Count('user'))

    def __str__ (self):
        return self.name + " - " + self.set_name + " - Price: " + str(self.price)# + " - Seller:\n " + str(self.user)


# after creating a new model we need to migrate it into the database.
# like this
# py manage.py makemigrations Magic
# py manage.py sqlmigrate Magic 0001(or what ever the migration number is)
# py manage.py migrate

# it is not yet migrated
# maybe we change the structure to user -> card, so there will be users and they will have cards that they can sell.
# first we should finish or at least countinue the tutorial ...
    


    