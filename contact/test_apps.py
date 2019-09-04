from django.apps import apps
from django.test import TestCase
from contact.apps import ContactConfig


class ContactAppConfigTest(TestCase):
    """Class for testing contacts app config"""

    def test_contact__app_config(self):
        self.assertEqual(ContactConfig.name, 'contact')
        self.assertEqual(apps.get_app_config('contact').name, 'contact')
