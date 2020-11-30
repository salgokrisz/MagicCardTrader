from django.test import TestCase
from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from users import views as UserViews
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from Magic.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your tests here.

class TestUrls(SimpleTestCase):

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

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('Magic:register')
        self.profile_url = reverse('Magic:profile')
        self.profile_cards_url = reverse('Magic:profile_cards')
        self.profile_purchases_url = reverse('Magic:profile_purchases')
        self.update_profile_url = reverse('Magic:update_profile')
        self.new_user = User.objects.create_user('test_user', 'test@test.com', 'pass')
        
    def test_register_GET(self):
        self.assertEquals(self.client.get(self.register_url).status_code, 200)
        self.assertTemplateUsed(self.client.get(self.register_url), 'users/register.html')
        self.assertEquals(UserRegisterForm.Meta.model, User)

    def test_new_user(self):
        self.assertEqual(User.objects.count(), 1)

    def test_login(self):
        self.login = self.client.login(username='test_user', password='pass')
        self.assertEqual(self.login, True)

    def test_profile_GET_logged_in(self):
        self.login = self.client.login(username='test_user', password='pass')
        self.assertEquals(self.client.get(self.profile_url).status_code, 200)
        self.assertTemplateUsed(self.client.get(self.profile_url), 'users/profile.html')

    def test_profile_cards_GET_logged_in(self):
        self.login = self.client.login(username='test_user', password='pass')
        self.assertEquals(self.client.get(self.profile_cards_url).status_code, 200)
        self.assertTemplateUsed(self.client.get(self.profile_cards_url), 'users/profile_cards.html')

    def test_profile_purchases_GET_logged_in(self):
        self.login = self.client.login(username='test_user', password='pass')
        self.assertEquals(self.client.get(self.profile_purchases_url).status_code, 200)
        self.assertTemplateUsed(self.client.get(self.profile_purchases_url), 'users/profile_purchases.html')

    def test_update_profile_GET_logged_in(self):
        self.login = self.client.login(username='test_user', password='pass')
        self.assertEquals(self.client.get(self.update_profile_url).status_code, 200)
        self.assertEquals(UserUpdateForm.Meta.model, User)

"""     def test_profile_GET_not_logged_in(self):
        self.assertEquals(self.client.get(self.profile_url).status_code, 302)

    def test_profile_cards_GET_not_logged_in(self):
        self.assertEquals(self.client.get(self.profile_cards_url).status_code, 302)

    def test_profile_purchases_GET_logged_in(self):
        self.assertEquals(self.client.get(self.profile_purchases_url).status_code, 302)
    
    def test_update_profile_GET_not_logged_in(self):
        self.assertEquals(self.client.get(self.update_profile_url).status_code, 302) """

class TestForms(TestCase):
    def test_user_register_form_is_valid(self):
        self.assertEquals(UserRegisterForm.Meta.model, User)
        form = UserRegisterForm(
            data={
                'username': 'test_user32054',
                'email': 'test_email@test.com',
                'password1': 'passWG123',
                'password2': 'passWG123',
            }
        )
        self.assertTrue(form.is_valid())

    def test_user_update_form_is_valid(self):
        self.assertEquals(UserUpdateForm.Meta.model, User)
        form = UserUpdateForm(
            data={
                'username': 'test_user',
                'email': 'test_email@test.com',
            }
        )
        self.assertTrue(form.is_valid())

    def test_profile_update_form_is_valid(self):
        im = Image.new(mode='RGB', size=(200, 200)) # create a new image using PIL
        im_io = BytesIO() # a BytesIO object for saving image
        im.save(im_io, 'JPEG') # save the image to im_io
        im_io.seek(0) # seek to the beginning
        image = InMemoryUploadedFile(
            im_io, None, 'random-name.jpg', 'image/jpeg', len(im_io.getvalue()), None
        )
        self.assertEquals(ProfileUpdateForm.Meta.model, Profile)
       
        file_dict = {
            'user_photo': image
        }
        form = ProfileUpdateForm(file_dict)
        self.assertTrue(form.is_valid())