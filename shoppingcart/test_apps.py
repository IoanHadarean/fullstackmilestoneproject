from django.apps import apps
from django.test import TestCase
from shoppingcart.apps import ShoppingcartConfig

class ShoppingcartConfigTest(TestCase):
    
    def test_contact_config(self):
        self.assertEqual(ShoppingcartConfig.name, 'shoppingcart')
        self.assertEqual(apps.get_app_config('shoppingcart').name, 'shoppingcart')