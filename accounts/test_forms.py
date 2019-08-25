from django.test import TestCase
from django import forms
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your tests here.

class TestUserRegistrationFrom(TestCase):
      
    def test_clean_email_return(self):
        form_params = {'username':'goagl', 'email':'hadareannelutu@yahoo.com', 'password1':'randompassword', 'password2':'randompassword2'}
        form = UserRegistrationForm(form_params)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.clean_email(), 'hadareannelutu@yahoo.com')

    def test_clean_passwords_match(self):
        form_params = {'username': 'goagl', 'email':'hadareannelutu@yahoo.com', 'password1':'randompassword', 'password2':'randompassword2'}
        form = UserRegistrationForm(form_params)
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(ValidationError, 'Passwords must match!', form.clean_passwords_match)

    def test_clean_passwords_match_return(self):
        form_params = {'username': 'goagl', 'email':'hadareannelutu@yahoo.com', 'password1':'randompassword2', 'password2':'randompassword2'}
        form = UserRegistrationForm(form_params)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean_passwords_match(), 'randompassword2')
