from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from .forms import UserLoginForm
from django.core.exceptions import ObjectDoesNotExist

# Create your tests here.

class LoginTest(TestCase):
    
    def setUp(self):
        self.credentials = {
            'username': 'user',
            'password': 'random'}
        user = User.objects.create_user(**self.credentials)
        user.save()
        self.invalid_credentials = {
            'username':'user2',
            'password':'random2'
        }
        
    def test_login(self):
        # send login data
        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)

    def test_invalid_login(self):
        response = self.client.post('/accounts/login/', self.invalid_credentials, follow=True)
        try:
            user = User.objects.get(username=self.invalid_credentials['username'])
        except ObjectDoesNotExist:
            self.assertFalse(response.context['user'].is_authenticated)
    
    def test_get_login_page(self):
        # Create an instance of a GET request.
        client = Client()
        response = client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)
