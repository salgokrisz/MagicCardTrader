from django.test import TestCase
from django.test import Client
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from . import views
from users import views as userViews


# Create your tests here.
class TestUrls(SimpleTestCase):
    #Tests For Magic App Urls
    def test_index_url_is_resolved(self):
        url = reverse('Magic:index')
        print(resolve(url))
        self.assertEquals(resolve(url).func, views.index)

    def test_users_url_is_resolved(self):
        url = reverse('Magic:users')
        print(resolve(url))
        self.assertEquals(resolve(url).func, views.users)

    def test_user_detail_url_is_resolved(self):
        url = reverse('Magic:user_detail', args=[10])
        print(resolve(url))
        self.assertEquals(resolve(url).func, views.user_detail)
    
    def test_cards_url_is_resolved(self):
        url = reverse('Magic:cards')
        print(resolve(url))
        self.assertEquals(resolve(url).func, views.cards)
    
    def test_card_detail_url_is_resolved(self):
        url = reverse('Magic:card_detail', args=[10])
        print(resolve(url))
        self.assertEquals(resolve(url).func, views.card_detail)

    def test_user_detail_cards_url_is_resolved(self):
        url = reverse('Magic:user_detail_cards', args=[10])
        print(resolve(url))
        self.assertEquals(resolve(url).func, views.user_detail_cards)
    
    def test_card_add_url_is_resolved(self):
        url = reverse('Magic:card_add')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, views.CardCreate)
    
    def test_address_add_url_is_resolved(self):
        url = reverse('Magic:create_address')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, views.AddressCreate)
    
    def test_card_delete_url_is_resolved(self):
        url = reverse('Magic:card_delete', args=[20])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, views.CardDelete)
    
    def test_card_update_url_is_resolved(self):
        url = reverse('Magic:card_update', args=[20])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, views.CardUpdate)

    #Tests For Users App Urls
    def test_register_url_resolved(self):
        url = reverse('Magic:register')
        self.assertEquals(resolve(url).func, userViews.register)

    def test_profile_url_resolved(self):
        url = reverse('Magic:profile')
        self.assertEquals(resolve(url).func, userViews.profile)

    def test_profile_cards_url_resolved(self):
        url = reverse('Magic:profile_cards')
        self.assertEquals(resolve(url).func, userViews.profile_cards)

    def test_profile_purchase_url_resolved(self):
        url = reverse('Magic:profile_purchases')
        self.assertEquals(resolve(url).func, userViews.profile_purchases)
    
    def test_update_profile_url_resolved(self):
        url = reverse('Magic:update_profile')
        self.assertEquals(resolve(url).func, userViews.update_profile)