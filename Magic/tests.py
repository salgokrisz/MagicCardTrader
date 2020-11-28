from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from Magic import views as MagicViews
from users import views as UserViews
from direct_messages import views as MessagesViews
from Magic.models import Profile, Address, Card
from Magic.forms import CardForm, AddressUpdateForm
import json
from django.contrib.auth.models import User
from django_countries import countries


# Create your tests here.
class TestUrls(SimpleTestCase):
    #Tests For Magic App Urls
    def test_index_url_is_resolved(self):
        url = reverse('Magic:index')
        self.assertEquals(resolve(url).func, MagicViews.index)

    def test_users_url_is_resolved(self):
        url = reverse('Magic:users')
        self.assertEquals(resolve(url).func, MagicViews.users)

    def test_user_detail_url_is_resolved(self):
        url = reverse('Magic:user_detail', args=[10])
        self.assertEquals(resolve(url).func, MagicViews.user_detail)
    
    def test_cards_url_is_resolved(self):
        url = reverse('Magic:cards')
        self.assertEquals(resolve(url).func, MagicViews.cards)
    
    def test_card_detail_url_is_resolved(self):
        url = reverse('Magic:card_detail', args=[10])
        self.assertEquals(resolve(url).func, MagicViews.card_detail)

    def test_user_detail_cards_url_is_resolved(self):
        url = reverse('Magic:user_detail_cards', args=[10])
        self.assertEquals(resolve(url).func, MagicViews.user_detail_cards)
    
    def test_card_add_url_is_resolved(self):
        url = reverse('Magic:card_add')
        self.assertEquals(resolve(url).func.view_class, MagicViews.CardCreate)
    
    def test_address_add_url_is_resolved(self):
        url = reverse('Magic:create_address')
        self.assertEquals(resolve(url).func.view_class, MagicViews.AddressCreate)
    
    def test_card_delete_url_is_resolved(self):
        url = reverse('Magic:card_delete', args=[20])
        self.assertEquals(resolve(url).func.view_class, MagicViews.CardDelete)
    
    def test_card_update_url_is_resolved(self):
        url = reverse('Magic:card_update', args=[20])
        self.assertEquals(resolve(url).func.view_class, MagicViews.CardUpdate)

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.users_url = reverse('Magic:users')
        self.cards_url = reverse('Magic:cards')
        #self.user_detail_url = reverse('Magic:user_detail', args=['10'])
        #self.card_detail_url = reverse('Magic:card_detail', args=[])
        self.card_create = MagicViews.CardCreate()
        self.card_update = MagicViews.CardUpdate()
        self.card_delete = MagicViews.CardDelete()
        self.address_update = MagicViews.AddressCreate()

    def test_users_GET(self):
        response = self.client.get(self.users_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'magic/users.html')
    
    def test_user_detail_GET_no_id(self):
        response = self.client.get('Magic:user_detail', args=[])
        self.assertEquals(response.status_code, 404)
        #self.assertTemplateUsed(response, 'magic/user_detail.html')

    def test_cards_GET(self):
        response = self.client.get(self.cards_url)
        self.assertAlmostEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'magic/cards.html')

    def test_card_detail_GET_no_id(self):
        #response = self.client.get(self.card_detail_url)
        response = self.client.get('Magic:card_detail', args=[])
        self.assertEquals(response.status_code, 404)

    def test_user_detail_cards_GET_no_id(self):
        response = self.client.get('Magic:user_detail_cards', args=[])
        self.assertEquals(response.status_code, 404)
        #self.assertTemplateUsed(response, 'magic/user_detail.html')

    def test_address_update(self):
        self.assertEqual(self.address_update.model, Address)
        self.assertEqual(self.address_update.form_class, AddressUpdateForm)

    def test_card_create(self):
        self.assertEqual(self.card_create.model, Card)
        self.assertEqual(self.card_create.form_class, CardForm)
        #self.assertEqual(self.view.context_object_name, 'add_cards')
        #self.assertEqual(self.view.template_name, 'magic/card_')

    def test_card_update(self):
        self.assertEqual(self.card_update.model, Card)

    def test_card_delete(self):
        self.assertEqual(self.card_delete.model, Card)
        

class TestForms(SimpleTestCase):

    def test_card_form_is_valid(self):
        self.assertEqual(CardForm.Meta.model, Card)
        form = CardForm(
            data={
                'name': 'some_card_name',
                'set_name': 'some_set_name',
                'price': 1200,
                'is_foil': False
            }
        )
        self.assertTrue(form.is_valid())

    def test_card_form_not_valid(self):
        form = CardForm(data={})
        self.assertFalse(form.is_valid())

    def test_address_form_not_valid(self):
        form = AddressUpdateForm(data={})
        self.assertFalse(form.is_valid())