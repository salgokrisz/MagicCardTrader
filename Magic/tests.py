from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from Magic import views as MagicViews
from users import views as UserViews
from direct_messages import views as MessagesViews
from shopping_cart import views as CartViews
from Magic.models import Profile, Address, Card
from Magic.forms import CardForm, AddressUpdateForm
import json
from django.contrib.auth.models import User


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

    #Tests For Users App Urls
    def test_register_url_resolved(self):
        url = reverse('Magic:register')
        self.assertEquals(resolve(url).func, UserViews.register)

    def test_profile_url_resolved(self):
        url = reverse('Magic:profile')
        self.assertEquals(resolve(url).func, UserViews.profile)

    def test_profile_cards_url_resolved(self):
        url = reverse('Magic:profile_cards')
        self.assertEquals(resolve(url).func, UserViews.profile_cards)

    def test_profile_purchase_url_resolved(self):
        url = reverse('Magic:profile_purchases')
        self.assertEquals(resolve(url).func, UserViews.profile_purchases)
    
    def test_update_profile_url_resolved(self):
        url = reverse('Magic:update_profile')
        self.assertEquals(resolve(url).func, UserViews.update_profile)

    #Test For Messages App Urls
    def test_inbox_url_resolved(self):
        url = reverse('Magic:inbox')
        self.assertEquals(resolve(url).func, MessagesViews.inbox)

    def test_directs_url_resolved(self):
        url = reverse('Magic:directs', args=[20])
        self.assertEquals(resolve(url).func, MessagesViews.directs)

    def test_send_url_resolved(self):
        url = reverse('Magic:send')
        self.assertEquals(resolve(url).func, MessagesViews.send_message)

    def test_new_url_resolved(self):
        url = reverse('Magic:new', args=[20])
        self.assertEquals(resolve(url).func, MessagesViews.new_conversation)

    #Test For Cart App Urls
    def test_add_url_resolved(self):
        url = reverse('Magic:add_to_cart', args=[20])
        self.assertEquals(resolve(url).func, CartViews.add_to_cart)

    def test_delete_url_resolved(self):
        url = reverse('Magic:delete_from_cart', args=[20])
        self.assertEquals(resolve(url).func, CartViews.delete_from_cart)

    def test_order_summary_url_resolved(self):
        url = reverse('Magic:order_summary')
        self.assertEquals(resolve(url).func.view_class, CartViews.OrderSummaryView)

    def test_checkout_url_resolved(self):
        url = reverse('Magic:checkout')
        self.assertEquals(resolve(url).func.view_class, CartViews.CheckoutView)

    def test_payment_url_resolved(self):
        url = reverse('Magic:payment')
        self.assertEquals(resolve(url).func.view_class, CartViews.PaymentView)

    """ def test_success_url_resolved(self):
        url = reverse('Magic:success')
        self.assertEquals(resolve(url).func, CartViews.success) """


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