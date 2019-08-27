from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.contrib import auth
from .forms import UserLoginForm, UserRegistrationForm
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile

# Create your tests here.


class LoginLogoutTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'user',
            'password': 'random'}
        user = User.objects.create_user(**self.credentials)
        user.save()
        self.invalid_credentials = {
            'username': 'user2',
            'password': 'random2'
        }

    def test_login_post_success(self):
        # send login data
        response = self.client.post('/accounts/login/',
                                    self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, '/accounts/profile/',
                             status_code=302, target_status_code=200)

    def test_user_can_login_and_logout(self):
        self.client.post('/accounts/login/', {'username': 'user',
                                              'password': 'random'})
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.client.post('/accounts/logout/')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)

    def test_redirect_user_if_authenticated(self):
        self.client.post('/accounts/login/', {'username': 'user',
                                              'password': 'random'})
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        response = self.client.post('/accounts/login/', {'username': 'user',
                                                         'password': 'random'})
        self.assertRedirects(response, '/accounts/profile/',
                             status_code=302, target_status_code=200)
        self.client.post('/accounts/logout/')

    def test_login_post_fail(self):
        response = self.client.post('/accounts/login/',
                                    self.invalid_credentials, follow=True)
        try:
            User.objects.get(username=self.invalid_credentials['username'])
        except ObjectDoesNotExist:
            self.assertFalse(response.context['user'].is_authenticated)

    def test_get_login_page(self):
        # Create an instance of a GET request.
        client = Client()
        response = client.get('/accounts/login/')
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertEquals(response.status_code, 200)


class RegistrationTest(TestCase):

    def setUp(self):
        self.credentials = {
                            'password1': '1375minglee',
                            'password2': '1375minglee',
                            'username': 'dasistmofaklaus',
                            'email': 'davai@example.com',
                           }
        self.invalid_credentials = {
                                    'password1': '88OidaAlwaysRemember',
                                    'password2': '1375minglee',
                                    'username': 'rushBNapoleon',
                                    'email': 'ArtyIsNotOp@example.com',
                                   }

    def test_get_registration_page(self):
        # Create an instance of a GET request.
        client = Client()
        response = client.get('/accounts/registration/')
        self.assertTemplateUsed(response, 'accounts/registration.html')
        self.assertEquals(response.status_code, 200)

    def test_registration_post_success(self):
        response = self.client.post('/accounts/registration/',
                                    self.credentials)
        self.assertRedirects(response, '/accounts/profile/')

    def test_redirect_user_if_authenticated(self):
        response = self.client.post('/accounts/registration/',
                                    self.credentials)
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        response = self.client.post('/accounts/registration/',
                                    self.credentials)
        self.assertRedirects(response, '/accounts/profile/')

    def test_registration_post_fail(self):
        response = self.client.post('/accounts/registration/',
                                    self.invalid_credentials)
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field='password2',
                             errors="The two password fields didn't match.")


class ProfileUpdateTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'user',
            'email': 'user@yahoo.com',
            'password': 'ComplexPassword'}
        user = User.objects.create_user(**self.credentials)
        user.save()
        self.user = {'username': 'complexUser', 'password': 'honoretpatria'}

    def test_profile_update(self):
        response = self.client.post('/accounts/profile/', self.user)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/')
        self.client.post('/accounts/login/', {'username': 'user',
                                              'password': 'ComplexPassword'})
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        update_url = '/accounts/profile/'

        # GET the form
        r = self.client.get(update_url)

        # retrieve form data as dict
        form = r.context['form']
        data = form.initial

        # manipulate data
        data['username'] = 'goagl'
        data['email'] = 'newemail@yahoo.com'

        # POST to the form
        r = self.client.post(update_url, {'username': data['username'],
                                          'email': data['email']})
        # retrieve again
        r = self.client.get(update_url)
        self.assertEqual(r.context['form'].initial['username'], 'goagl')
        self.assertEqual(r.context['form'].initial['email'], 'newemail@yahoo.com')
