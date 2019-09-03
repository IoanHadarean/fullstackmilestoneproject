from django.test import TestCase
from django import forms
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class TestUserRegistrationForm(TestCase):
    """Class for testing user registration form"""

    """Test clean email method of user registration form (unique email)"""
    def test_clean_email_return(self):
        form_params = {'username': 'goagl', 'email': 'hadareannelutu@yahoo.com', 'password1': 'randompassword', 'password2': 'randompassword2'}
        form = UserRegistrationForm(form_params)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.clean_email(), 'hadareannelutu@yahoo.com')

    """Test clean passwords match method of user registration form (matching passwords) """
    def test_clean_passwords_match(self):
        form_params = {'username': 'goagl', 'email': 'hadareannelutu@yahoo.com', 'password1': 'randompassword', 'password2': 'randompassword2'}
        form = UserRegistrationForm(form_params)
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(ValidationError, 'Passwords must match!', form.clean_passwords_match)

    """Test clean password match method return"""
    def test_clean_passwords_match_return(self):
        form_params = {'username': 'goagl', 'email': 'hadareannelutu@yahoo.com', 'password1': 'randompassword2', 'password2': 'randompassword2'}
        form = UserRegistrationForm(form_params)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean_passwords_match(), 'randompassword2')
