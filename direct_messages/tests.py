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
        self.directs = reverse('Magic:directs', args=[self.user2.username])
        self.send_msg = reverse('Magic:send')
        self.new = reverse('Magic:new', args=[self.user2.username])
        self.login = self.client.login(username='test_user', password='pass')

    def test_inbox(self):
        self.assertEquals(self.client.get(self.inbox).status_code, 200)
        self.assertTemplateUsed(self.client.get(self.inbox), 'direct_messages/messages.html')

    def test_directs(self):
        self.assertEquals(self.client.get(self.directs).status_code, 200)
        #self.assertRedirects(self.client.get(self.directs), '/messages/' + self.user2.username + '/$', status_code=200)

    def test_send_msg(self):
        self.client.post(reverse('Magic:directs', args=[self.user2.username]), kwargs={'content': 'content'})
        self.assertRedirects(self.client.get(self.send_msg), '/messages/$', status_code=302)

    def test_new_conversation(self):
        self.assertRedirects(self.client.get(self.new), '/messages/' + self.user2.username + '/$', status_code=302)

    def test_new_conversation_no_valid_target_user(self):
        self.assertRedirects(self.client.get(reverse('Magic:new', args=['not_valid_username'])), '/messages/$', status_code=302)