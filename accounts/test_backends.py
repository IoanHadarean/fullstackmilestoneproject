from django.test import TestCase
from .backends import EmailAuth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your tests here.

class TestBackends(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'KastaraWasTaken',
            'email': 'kastara@yahoo.com',
            'password': 'MemoriesRemain'}
        user = User.objects.create_user(**self.credentials)
        user.save()
    
    def test_email_auth_authenticate(self):
        self.assertEquals(EmailAuth.authenticate(self, username='kastara@yahoo.com',
                                                 password='MemoriesRemain'),
                                                 User.objects.get(username='KastaraWasTaken'))
        self.assertEquals(EmailAuth.authenticate(self, username='poggers@yahoo.com',
                                                 password='MemoriesRemain'),
                                                 None)
        self.assertEquals(EmailAuth.authenticate(self, username='kastara@yahoo.com',
                                                 password='OnceUponATimeInBrooklyn'),
                                                 None)

    def test_email_auth_get_user(self):
        self.assertEquals(EmailAuth.get_user(self, user_id=1),
                                             User.objects.get(username='KastaraWasTaken'))
        self.assertEquals(EmailAuth.get_user(self, user_id=2), None)
        user = User.objects.get(username='KastaraWasTaken')
        user.is_active = False
        user.save()
        self.assertEquals(EmailAuth.get_user(self, user_id=1), None)