from django.db import models
from django.db.models import Count
from django.urls import reverse
from mtgsdk import Card
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    user_photo = models.FileField(upload_to='profile_images', default='profile_images/default-profile-picture.jpg')
    date_registered = models.DateTimeField(auto_now_add=True, blank=True)
    address = models.TextField()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save() 

    def __str__ (self):
        return self.user.username# + " - Cards for sale: " + str(self.available_cards)#str(Card.objects.annotate(total=Count('user')))


'''
def get_image_url(name, set_name):
        listOfVersions = []
        versions = Card.where(name=name, set=set_name).all()
        for card in versions:
            listOfVersions.append(card.image_url)
        listOfVersions = list(dict.fromkeys(listOfVersions))
        print(listOfVersions)
        return listOfVersions
'''
class Card(models.Model):
    name = models.CharField(max_length = 150)
    set_name = models.CharField(max_length = 150)
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_foil = models.BooleanField(default=False)
    is_ordered = models.BooleanField(default=False)
    #imageUrl = models.TextField(default=get_image_url(name, set_name))


    def get_absolute_url(self):
        return reverse('Magic:user_detail', kwargs={'user_id': self.user.id})

    @classmethod
    def user_cards(self):
        return Card.objects.annotate(total=Count('user'))

    def __str__ (self):
        return self.name + " - " + self.set_name + " - Price: " + str(self.price)# + " - Seller:\n " + str(self.user)

class CardPhoto(models.Model):
    photo = models.FileField(upload_to='card_photos', default='card_photos/Magic_card_back.jpg')

# after creating a new model we need to migrate it into the database.
# like this
# py manage.py makemigrations Magic
# py manage.py sqlmigrate Magic 0001(or what ever the migration number is)
# py manage.py migrate

# it is not yet migrated
# maybe we change the structure to user -> card, so there will be users and they will have cards that they can sell.
# first we should finish or at least countinue the tutorial ...
    


    