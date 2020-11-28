from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from direct_messages import views as MessagesViews
import json
from django.contrib.auth.models import User
from django_countries import countries

# Create your tests here.
class TestUrls(SimpleTestCase):

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

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', 'test@test.com', 'pass')
        self.user2 = User.objects.create_user('test_user2', 'test2@test.com', 'pass2')
        self.inbox = reverse('Magic:inbox')
        self.directs = reverse('Magic:directs', args=[10])

    def test_inbox_logged_in(self):
        self.login = self.client.login(username='test_user', password='pass')
        self.assertEquals(self.client.get(self.inbox).status_code, 200)

    def test_directs_logged_in(self):
        self.login = self.client.login(username='test_user', password='pass')
        self.assertEquals(self.client.get(self.directs).status_code, 200)

    