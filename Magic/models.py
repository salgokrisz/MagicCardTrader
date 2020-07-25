from django.db import models


class User(models.Model):
    name = models.CharField(max_length = 250)
    email_address = models.CharField(max_length = 500)
    available_cards = models.IntegerField()

    def __str__ (self):
        return "Name: " + self.name + " - Cards for sale: " + str(self.available_cards)



class CardsForSale (models.Model):
    card_name = models.CharField(max_length = 150)
    set_name = models.CharField(max_length = 150)
    price = models.IntegerField()
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# after creating a new model we need to migrate it into the database.
# like this
# py manage.py makemigrations Magic
# py manage.py sqlmigrate Magic 0001(or what ever the migration number is)
# py manage.py migrate

# it is not yet migrated
# maybe we change the structure to user -> card, so there will be users and they will have cards that they can sell.
# first we should finish or at least countinue the tutorial ...
    


    