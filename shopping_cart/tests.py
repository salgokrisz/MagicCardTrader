from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from shopping_cart import views as CartViews
from shopping_cart.templatetags import shopping_cart_template_tags
from django.contrib.auth.models import User
from Magic.models import Card
from shopping_cart.forms import CheckoutForm

# Create your tests here.

class TestUrls(SimpleTestCase):
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

@classmethod
class TestViews(TestCase):
    def setUpTestData(cls):
        cls.user = User.objects.create_user('test_user', 'test@test.com', 'pass')
        cls.card = Card.objects.create(name="card_name", set_name='set_name', price=10, user=cls.user, is_foil=True, is_ordered=False, image_url='')

    def setUp(self):
        self.client = Client()
        #self.new_user = User.objects.create_user('test_user', 'test@test.com', 'pass')
        #self.new_card = Card.objects.create(name="card_name", set_name='set_name', price=10, user=self.new_user, is_foil=True, is_ordered=False, image_url='')
        self.add_to_cart_url = reverse('Magic:add_to_cart', self.card)
        self.delete_from_cart_url = reverse('Magic:delete_from_cart', self.new_card)
        self.order_summary_view = CartViews.OrderSummaryView()
        self.checkout_view = CartViews.CheckoutView()
        self.payment_view = CartViews.PaymentView()
    
    def test_add_to_cart_GET_logged_in(self):
        self.login = self.client.login(username='test_user', password='pass')
        self.assertEquals(self.client.get(self.add_to_cart_url).status_code, 302)
        self.assertEquals(self.client.get(shopping_cart_template_tags.cart_item_counter(self.user), 1))
        self.assertRedirects(self.client.get(self.add_to_cart_url), 'Magic:cards', status_code=302)
    
    def test_add_to_cart_GET_not_logged_in(self):
        self.assertRedirects(self.client.get(self.add_to_cart_url), 'Magic:login', status_code=302)

    def test_delete_from_cart_GET_logged_in(self):
        self.login = self.client.login(username='test_user', password='pass')
        self.assertRedirects(self.client.get(self.add_to_cart_url), 'Magic:order_summary', status_code=302)
        self.assertEquals(self.client.get(shopping_cart_template_tags.cart_item_counter(self.user), 0))

    def test_delete_from_cart_GET_not_logged_in(self):
        self.assertRedirects(self.client.get(self.add_to_cart_url), 'Magic:login', status_code=302)

    def test_checkout_view_form_is_valid(self):
        self.login = self.client.login(username='test_user', password='pass')
        form = CheckoutForm(
            data={
                'first_name':'first_name',
                'last_name':'last_name',
                'street_address':'street_address',
                'apartment_number':'123/B',
                'country':'HU',
                'zip_code':'123'
            }
        )
        self.assertTrue(form.is_valid())
        self.assertRedirects(self.client.get(self.checkout_view), 'Magic:checkout', status_code=302)
