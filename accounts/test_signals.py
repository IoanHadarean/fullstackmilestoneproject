from django.test import TestCase
from django.db.models.signals import post_save
from .models import Profile
from django.dispatch import receiver
from django.contrib.auth.models import User
from unittest import mock
from contextlib import contextmanager
from .signals import save_profile

# Create your tests here.

class TestUserRegistrationFrom(TestCase):

    def test_save_profile(self):
        user = User.objects.create_user('john', 'john@doe.com', 'password')
        user.save()
        self.assertRaises(Profile.DoesNotExist, save_profile(sender=user, instance=user))
        