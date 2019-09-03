from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import UserLoginForm, UserRegistrationForm
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile
from django.contrib.messages import get_messages


class LoginLogoutTest(TestCase):
    """Class for testing login/logout process"""

    """Set up the login/logout credentials and user"""
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

    """Test the successful login of a user"""
    def test_login_post_success(self):
        response = self.client.post('/accounts/login/',
                                    self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have successfully logged in!")
        self.assertRedirects(response, '/accounts/profile/',
                             status_code=302, target_status_code=200)

    """Test if the user can logout after login"""
    def test_user_can_login_and_logout(self):
        self.client.post('/accounts/login/', {'username': 'user',
                                              'password': 'random'})
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.client.post('/accounts/logout/')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)

    """
    Test redirection for user to profile if he/she is already authenticated
    and tries to access the login page again
    """
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

    """Test failed login for user in case of invalid credentials"""
    def test_login_post_fail(self):
        response = self.client.post('/accounts/login/',
                                    self.invalid_credentials, follow=True)
        try:
            User.objects.get(username=self.invalid_credentials['username'])
        except ObjectDoesNotExist:
            self.assertFalse(response.context['user'].is_authenticated)

    """Test get login page view"""
    def test_get_login_page(self):
        response = self.client.get('/accounts/login/')
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertEquals(response.status_code, 200)


class RegistrationTest(TestCase):
    """Class for testing the registration process"""

    """Set up the valid and invalid credentials for registration"""
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

    """Test get registration page view"""
    def test_get_registration_page(self):
        response = self.client.get('/accounts/registration/')
        self.assertTemplateUsed(response, 'accounts/registration.html')
        self.assertEquals(response.status_code, 200)

    """Test the successful registration of a user"""
    def test_registration_post_success(self):
        response = self.client.post('/accounts/registration/',
                                    self.credentials)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have successfully registered! We have sent you a confirmation email!")
        self.assertRedirects(response, '/accounts/profile/')

    """
    Test redirection for user to profile if he/she is already authenticated
    and tries to access the registration page again
    """
    def test_redirect_user_if_authenticated(self):
        response = self.client.post('/accounts/registration/',
                                    self.credentials)
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        response = self.client.post('/accounts/registration/',
                                    self.credentials)
        self.assertRedirects(response, '/accounts/profile/')

    """Test the unsuccessful registration of a user (password fields don't match)"""
    def test_registration_post_fail(self):
        response = self.client.post('/accounts/registration/',
                                    self.invalid_credentials)
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field='password2',
                             errors="The two password fields didn't match.")


class ProfileUpdateTest(TestCase):
    """Class for testing profile update"""

    """Set up the credentials for logging in the user"""
    def setUp(self):
        self.credentials = {
            'username': 'user',
            'email': 'user@yahoo.com',
            'password': 'ComplexPassword'}
        user = User.objects.create_user(**self.credentials)
        user.save()
        self.user = {'username': 'complexUser', 'password': 'honoretpatria'}

    """
    Test profile update after the user is logged in
    If the user is not logged in he/she is redirected
    to the login page
    """
    def test_profile_update(self):
        response = self.client.post('/accounts/profile/', self.user)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/')
        self.client.post('/accounts/login/', {'username': 'user',
                                              'password': 'ComplexPassword'})
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        update_url = '/accounts/profile/'

        # GET the profile update form
        res = self.client.get(update_url)

        # Retrieve form data as dict
        form = res.context['form']
        data = form.initial

        # Manipulate the form username and email
        data['username'] = 'goagl'
        data['email'] = 'newemail@yahoo.com'

        # POST the new username and email to the form
        res = self.client.post(update_url, {'username': data['username'],
                                            'email': data['email']})
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your account has been updated!")

        # Retrieve the username and email again
        res = self.client.get(update_url)
        self.assertEqual(res.context['form'].initial['username'], 'goagl')
        self.assertEqual(res.context['form'].initial['email'], 'newemail@yahoo.com')
