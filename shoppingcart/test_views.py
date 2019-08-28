from django.test import TestCase
from .views import create_ref_code, is_valid_form, fetchCards, delete_card, save_default_card
from accounts.models import Profile
from django.contrib.auth.models import User
from .models import Order, Address
from .forms import CheckoutForm
from django.test import RequestFactory
from django.test.client import Client
from django.contrib.messages.storage.fallback import FallbackStorage
import stripe
import pytz
import datetime


class CheckoutViewTest(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.code = create_ref_code()
        self.valid = is_valid_form(['', ''])
        self.credentials = {
            'username': 'User3457',
            'password': 'randompassword678'}
        self.user = User.objects.create_user(**self.credentials)
        self.user.save()
        self.checkout_form1 = {
            'shipping_address': '1A Bridge Road',
            'shipping_address2': 'Gillingham',
            'shipping_zip_code': 'ME6 1KJ',
            'shipping_country': 'UK',
            'same_billing_address': True,
            'payment_option': 'S',
        }
        self.checkout_form2 = {
            'same_billing_address': False,
            'use_default_shipping': True,
            'use_default_billing': True,
            'payment_option': 'S',
        }
        self.checkout_form3 = {
            'shipping_address': '1A Bridge Road',
            'shipping_address2': 'Gillingham',
            'shipping_zip_code': 'ME6 1KJ',
            'shipping_country': 'UK',
            'billing_address': '1A Bridge Road',
            'billing_address2': 'Gillingham',
            'billing_zip_code': 'ME6 1KJ',
            'billing_country': 'UK',
            'set_default_shipping': True,
            'set_default_billing': True,
            'same_billing_address': False,
            'payment_option': 'S',
        }
        self.checkout_form4 = {
            'same_billing_address': True,
            'use_default_shipping': True,
            'use_default_billing': True,
            'payment_option': 'S',
        }
        self.checkout_form5 = {
            'shipping_address': '1A Bridge Road',
            'shipping_address2': 'Gillingham',
            'shipping_zip_code': 'ME6 1KJ',
            'shipping_country': 'UK',
            'billing_address': '1A Bridge Road',
            'billing_address2': 'Gillingham',
            'billing_zip_code': 'ME6 1KJ',
            'billing_country': 'UK',
            'set_default_shipping': True,
            'set_default_billing': True,
            'same_billing_address': True,
            'payment_option': 'S',
        }
        self.checkout_form6 = {
            'payment_option': 'S',
            'same_billing_address': True,
            'shipping_address': '1A Bridge Road',
            'shipping_address2': '',
            'shipping_zip_code': '',
            'shipping_country': 'UK',
        }
        self.checkout_form7 = {
            'payment_option': 'S',
            'same_billing_address': False,
            'shipping_address': '1A Bridge Road',
            'shipping_address2': '',
            'shipping_zip_code': '',
            'shipping_country': 'UK',
        }
        self.checkout_form8 = {
            'shipping_address': '1A Bridge Road',
            'shipping_address2': 'Medway',
            'shipping_zip_code': 'ME7 6KU',
            'shipping_country': 'UK',
            'billing_address': '1A Bridge Road',
            'billing_address2': '',
            'billing_zip_code': '',
            'billing_country': 'UK',
            'payment_option': 'S',
            'same_billing_address': False,
        }
        self.checkout_form9 = {}
        self.checkout_form10 = {
            'same_billing_address': False,
            'use_default_shipping': False,
            'shipping_address': '1A Bridge Road',
            'shipping_address2': 'Gillingham',
            'shipping_zip_code': 'ME6 1KJ',
            'shipping_country': 'UK',
            'use_default_billing': True,
            'payment_option': 'S',
        }

    def test_create_ref_code(self):
        self.assertEqual(len(self.code), 20)
        
    def test_is_valid_form(self):
        self.assertEqual(self.valid, False)
        
    def test_checkout_view_get_fail(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        response = self.client.get('/shoppingcart/checkout/')
        self.assertRedirects(response, '/shoppingcart/checkout/', status_code=302, target_status_code=302)

    def test_checkout_view_get_success(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=500, ordered_date=datetime.datetime(2019, 7, 25, tzinfo=pytz.UTC))
        order.save()
        default_shipping_address = Address(user=self.user, address_type='S',
                                                default=True)
        default_shipping_address.save()
        default_billing_address = Address(user=self.user, address_type='B',
                                                default=True)
        default_billing_address.save()
        response = self.client.get('/shoppingcart/checkout/')
        self.assertTemplateUsed(response, 'shoppingcart/checkout.html')

    def test_checkout_post_fail_no_order(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form1)
        self.assertRedirects(response, '/shoppingcart/order_summary/', status_code=302, target_status_code=302)

    def test_checkout_post_success_same_billing_address(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=500, 
                      ordered_date=datetime.datetime(2019, 7, 25, tzinfo=pytz.UTC), 
                      ordered=False, save_default_billing=True, use_default_billing=True)
        order.save()
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form1)
        self.assertRedirects(response, '/shoppingcart/payment/stripe/')

    def test_checkout_post_success_not_same_billing_use_default_shipping_and_billing(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=600, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False, save_default_shipping=True, save_default_billing=True)
        order.save()
        default_shipping_address = Address(user=self.user, address_type='S',
                                           default=True)
        default_shipping_address.save()
        default_billing_address = Address(user=self.user, address_type='B',
                                          default=True)
        default_billing_address.save()
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form2)
        self.assertRedirects(response, '/shoppingcart/payment/stripe/')
        
    def test_checkout_post_fail_not_same_billing_no_default_shipping(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=600, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False, save_default_shipping=True, save_default_billing=True)
        order.save()
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form2)
        self.assertRedirects(response, '/shoppingcart/checkout/')
        
    def test_checkout_post_fail_not_same_billing_no_default_billing(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=600, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False, save_default_shipping=True, save_default_billing=True)
        order.save()
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form10)
        self.assertRedirects(response, '/shoppingcart/checkout/')
        
    def test_checkout_post_success_not_same_billing_update_default_shipping_and_billing(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=700, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        default_shipping_address = Address(user=self.user, address_type='S',
                                                default=True)
        default_shipping_address.save()
        default_billing_address = Address(user=self.user, address_type='B',
                                                default=True)
        default_billing_address.save()
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form3)
        self.assertRedirects(response, '/shoppingcart/payment/stripe/')
        
    def test_checkout_post_success_not_same_billing_save_default_shipping_and_billing(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=700, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form3)
        self.assertRedirects(response, '/shoppingcart/payment/stripe/')
        
    def test_checkout_post_success_same_billing_use_default_shipping_and_billing(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=600, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False, save_default_shipping=True)
        order.save()
        default_shipping_address = Address(user=self.user, address_type='S',
                                                default=True)
        default_shipping_address.save()
        default_billing_address = Address(user=self.user, address_type='B',
                                                default=True)
        default_billing_address.save()
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form4)
        self.assertRedirects(response, '/shoppingcart/payment/stripe/')
        
    def test_checkout_post_fail_same_billing_no_default_shipping_and_billing(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=600, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False, save_default_shipping=True)
        order.save()
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form4)
        self.assertRedirects(response, '/shoppingcart/checkout/')
        
    def test_checkout_post_success_same_billing_update_default_shipping_and_billing(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=700, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False, use_default_shipping=True)
        order.save()
        default_shipping_address = Address(user=self.user, address_type='S',
                                                default=True)
        default_shipping_address.save()
        default_billing_address = Address(user=self.user, address_type='B',
                                                default=True)
        default_billing_address.save()
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form5)
        self.assertRedirects(response, '/shoppingcart/payment/stripe/')
        
    def test_checkout_post_success_same_billing_save_default_shipping_and_billing(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=700, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False, use_default_shipping=True)
        order.save()
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form5)
        self.assertRedirects(response, '/shoppingcart/payment/stripe/')
        
    def test_checkout_post_fail_same_billing_no_shipping_address(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=700, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form6)
        self.assertRedirects(response, '/shoppingcart/checkout/')
        
    def test_checkout_post_fail_not_same_billing_invalid_shipping_address(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=700, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form7)
        self.assertRedirects(response, '/shoppingcart/checkout/')
        
    def test_checkout_post_fail_not_same_billing_invalid_billing_address(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=700, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form8)
        self.assertRedirects(response, '/shoppingcart/checkout/')
        
    def test_checkout_post_fail_invalid_data(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=700, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.post('/shoppingcart/checkout/', self.checkout_form9)
        self.assertRedirects(response, '/shoppingcart/checkout/')
        
        
class CardHandlersTest(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.credentials = {
            'username': 'User3457',
            'password': 'randompassword678'}
        self.user = User.objects.create_user(**self.credentials)
        self.user.save()
        self.profile = Profile(user=self.user, stripe_customer_id='cus_FgoD0vvyFVxqIP')
        
    def test_delete_card(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        profile = Profile.objects.all()[0]
        profile.stripe_customer_id = 'cus_FgoD0vvyFVxqIP'
        profile.save()
        card_list = fetchCards(self.profile)
        customer = stripe.Customer.retrieve(profile.stripe_customer_id)
        token = stripe.Token.create(
                card={
                    'number': '4242424242424242',
                    'exp_month': 12,
                    'exp_year': 2020,
                    'cvc': '123',
                    },
                )
        customer.sources.create(source=token)
        delete_card(request, card_list[1].id)
        
    def test_fetch_cards(self):
        card_list = fetchCards(self.profile)
        self.assertEqual(len(card_list), 3)
        
    def test_save_default_card(self):
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        profile = Profile.objects.all()[0]
        profile.stripe_customer_id = 'cus_FgoD0vvyFVxqIP'
        profile.save()
        card_list = fetchCards(self.profile)
        save_default_card(request, card_list[2].id)
        
        
        
        
        
        
        
        