from django.test import TestCase
from .views import create_ref_code, is_valid_form, fetchCards, delete_card, save_default_card
from .views import item_detail
from accounts.models import Profile
from django.contrib.auth.models import User
from .models import Order, Address, OrderItem, Order, Item, Coupon,  UserCoupon
from .forms import CheckoutForm
from django.test import RequestFactory
from django.test.client import Client
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
import stripe
import pytz
import datetime


class CheckoutProcessTest(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.code = create_ref_code()
        self.valid = is_valid_form(['', ''])
        self.credentials = {
            'username': 'User3457',
            'password': 'randompassword678'}
        self.user = User.objects.create_user(**self.credentials)
        self.user.save()
        self.coupon = Coupon(code='WEDDING', amount=300, valid_from=datetime.datetime(2019, 8, 29, tzinfo=pytz.UTC),
                             valid_to=datetime.datetime(2020, 8, 24, tzinfo=pytz.UTC), active=True)
        self.coupon.save()
        self.coupon2 = Coupon(code='WEDDING_PLANNER', amount=100, valid_from=datetime.datetime(2019, 8, 29, tzinfo=pytz.UTC),
                             valid_to=datetime.datetime(2020, 8, 24, tzinfo=pytz.UTC), active=True)
        self.coupon2.save()
        self.user_coupon = UserCoupon(user=self.user, coupon=self.coupon)
        self.user_coupon.save()
        self.shirt = Item(title='Shirt', price=300.0, category='Shirts', label='primary', slug='random-slug', description='shirt')
        self.shirt.image = SimpleUploadedFile(name='BE266_rose_top.jpg', 
                                          content=open('/home/ubuntu/environment/ecommerce/media/random.jpg', 'rb').read(),
                                          content_type='image/jpeg')
        self.shirt.save()
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
        
    def test_order_summary_view_get_success(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=500, ordered_date=datetime.datetime(2019, 7, 25, tzinfo=pytz.UTC))
        order.save()
        response = self.client.get('/shoppingcart/order_summary/')
        self.assertTemplateUsed(response, 'shoppingcart/order_summary.html')
        
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
        
    def test_add_coupon_post_fail_no_order(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        response = self.client.post('/shoppingcart/add_coupon/', {'code': 'WEDDING'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You do not have an active order')
        self.assertRedirects(response, '/shoppingcart/checkout/', status_code=302, target_status_code=302)
        
    def test_add_coupon_post_fail_no_coupon(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=700, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.post('/shoppingcart/add_coupon/', {'code': 'WEDDING_FIESTA'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'This coupon does not exist or is no longer active')
        self.assertRedirects(response, '/shoppingcart/checkout/')
        
    def test_add_coupon_post_fail_coupon_amount_exceeds_or_equals_order_value(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        orderitem = OrderItem(user=self.user, ordered=False, item=self.shirt, quantity=1)
        orderitem.save()
        order = Order(user=self.user, ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        order.items.add(orderitem)
        order.save()
        response = self.client.post('/shoppingcart/add_coupon/', {'code': 'WEDDING'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You can not use this coupon for items with the price less than or equal to the value of the coupon')
        self.assertRedirects(response, '/shoppingcart/checkout/')
        
    def test_add_coupon_post_fail_order_already_has_coupon(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, used_coupon=True, ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.post('/shoppingcart/add_coupon/', {'code': 'WEDDING'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You can not use more than one coupon for an order')
        self.assertRedirects(response, '/shoppingcart/checkout/')
    
    def test_add_coupon_post_fail_add_same_coupon_order_coupon_limit(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        orderitem = OrderItem(user=self.user, ordered=False, item=self.shirt, quantity=2)
        orderitem.save()
        order = Order(user=self.user, used_coupon=True, ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        order.items.add(orderitem)
        order.save()
        response = self.client.post('/shoppingcart/add_coupon/', {'code': 'WEDDING'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You can not use more than one coupon for an order')
        self.assertRedirects(response, '/shoppingcart/checkout/')
    
    def test_add_coupon_post_fail_add_different_coupon_order_coupon_limit(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        orderitem = OrderItem(user=self.user, ordered=False, item=self.shirt, quantity=2)
        orderitem.save()
        order = Order(user=self.user, used_coupon=True, ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        order.items.add(orderitem)
        order.save()
        response = self.client.post('/shoppingcart/add_coupon/', {'code': 'WEDDING_PLANNER'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You can not use more than one coupon for an order')
        self.assertRedirects(response, '/shoppingcart/checkout/')
        
    def test_add_coupon_post_fail_already_used_coupon(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        self.user_coupon.is_used = True
        self.user_coupon.save()
        orderitem = OrderItem(user=self.user, ordered=False, item=self.shirt, quantity=2)
        orderitem.save()
        order = Order(user=self.user, used_coupon=False, ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        order.items.add(orderitem)
        order.save()
        response = self.client.post('/shoppingcart/add_coupon/', {'code': 'WEDDING'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have already used this coupon')
        self.assertRedirects(response, '/shoppingcart/checkout/')

    def test_add_coupon_post_success(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        orderitem = OrderItem(user=self.user, ordered=False, item=self.shirt, quantity=2)
        orderitem.save()
        order = Order(user=self.user, used_coupon=False, ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        order.items.add(orderitem)
        order.save()
        response = self.client.post('/shoppingcart/add_coupon/', {'code': 'WEDDING'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Successfully added coupon')
        self.assertRedirects(response, '/shoppingcart/checkout/')
        
        
class CardHandlersTest(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.credentials = {
            'username': 'User3457',
            'password': 'randompassword678'}
        self.user = User.objects.create_user(**self.credentials)
        self.user.save()
        self.profile = Profile(user=self.user, stripe_customer_id='cus_FiLOa8AfQAfwNI')
        customer_profile = Profile.objects.all()[0]
        customer_profile.stripe_customer_id = 'cus_FiLOa8AfQAfwNI'
        customer_profile.one_click_purchasing = True
        customer_profile.save()
        
    def test_delete_card(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        profile = Profile.objects.all()[0]
        profile.stripe_customer_id = 'cus_FiLOa8AfQAfwNI'
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
        profile.stripe_customer_id = 'cus_FiLOa8AfQAfwNI'
        profile.save()
        card_list = fetchCards(self.profile)
        save_default_card(request, card_list[2].id)
        
    def test_update_card_view_get_success(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        response = self.client.get('/shoppingcart/update_card/card_1FCukOF3JWQSMs3R5GHJkEuL/')
        self.assertTemplateUsed(response, 'shoppingcart/update_card.html')
    
    def test_update_card_post_fail_invalid_card_details(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=700, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.post('/shoppingcart/update_card/card_1FCukOF3JWQSMs3R5GHJkEuL/', {})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid credit card details')
        self.assertRedirects(response, '/shoppingcart/payment/stripe/', status_code=302, target_status_code=302)
    
    def test_update_card_post_success(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        profile = Profile.objects.all()[0]
        profile.stripe_customer_id = 'cus_FiLOa8AfQAfwNI'
        profile.save()
        order = Order(user=self.user, amount=700, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        card_list = fetchCards(profile)
        update_card_url = '/shoppingcart/update_card/{}/'.format(card_list[0].id)
        response = self.client.post(update_card_url, {'stripeToken': 'tok_visa'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your card details have been updated successfully')
        self.assertRedirects(response, '/shoppingcart/payment/stripe/', status_code=302, target_status_code=302)

class PaymentViewTest(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.credentials = {
            'username': 'User3457',
            'password': 'randompassword678'}
        self.user = User.objects.create_user(**self.credentials)
        self.user.save()
        self.new_credentials = {
            'username': 'newuser34',
            'email': 'newuser34@yahoo.com',
            'password': '789Gyuiop'
        }
        self.new_user = User.objects.create_user(**self.new_credentials)
        self.new_user.save()
        self.profile = Profile(user=self.user)
        self.new_profile = Profile(user=self.new_user)
        customer_profile = Profile.objects.all()[0]
        customer_profile.stripe_customer_id = 'cus_FiLOa8AfQAfwNI'
        customer_profile.one_click_purchasing = True
        customer_profile.save()
        self.shirt = Item(title='Shirt', price=300.0, category='Shirts', label='primary', slug='random-slug', description='shirt')
        self.shirt.image = SimpleUploadedFile(name='BE266_rose_top.jpg', 
                                           content=open('/home/ubuntu/environment/ecommerce/media/random.jpg', 'rb').read(),
                                           content_type='image/jpeg')
        self.shirt.save()
        self.payment_form1 = {
            'stripeToken': 'tok_visa',
            'save': True,
            'use_default': False
        }
        self.payment_form2 = {'token': ''}

    def test_payment_view_get_fail(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=700, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.get('/shoppingcart/payment/stripe/')
        self.assertRedirects(response, '/shoppingcart/checkout/')
        
    def test_payment_view_get_success(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        order = Order(user=self.user, amount=700, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        billing_address = Address(user=self.user, address_type='B',
                                         default=True)
        billing_address.save()
        order.billing_address = billing_address
        order.save()
        response = self.client.get('/shoppingcart/payment/stripe/')
        self.assertTemplateUsed(response, 'shoppingcart/payment.html')
        
    def test_payment_post_fail_card_limit(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        order = Order(user=self.user, amount=700, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.post('/shoppingcart/payment/stripe/', self.payment_form1)
        self.assertRedirects(response, '/shoppingcart/payment/stripe/', status_code=302, target_status_code=302)
        
    def test_payment_post_success_save_new_customer(self):
        self.client.post('/accounts/login/', self.new_credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        orderitem = OrderItem(user=self.new_user, ordered=False, item=self.shirt, quantity=1)
        orderitem.save()
        order = Order(id=1, user=self.new_user, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        order.items.add(orderitem)
        order.save()
        response = self.client.post('/shoppingcart/payment/stripe/', self.payment_form1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your order was successful! We have sent you a confirmation email')
        self.assertRedirects(response, '/')
        
    def test_payment_post_fail_invalid_parameters(self):
        self.client.post('/accounts/login/', self.new_credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        order = Order(id=1, user=self.new_user, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.post('/shoppingcart/payment/stripe/', self.payment_form1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid parameters')
        self.assertRedirects(response, '/')
        

class CartProcessTest(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.credentials = {
            'username': 'User3457',
            'password': 'randompassword678'}
        self.user = User.objects.create_user(**self.credentials)
        self.user.save()
        self.shirt = Item(title='Shirt', price=300.0, category='Shirts', label='primary', slug='random-slug', description='shirt')
        self.shirt.image = SimpleUploadedFile(name='BE266_rose_top.jpg', 
                                          content=open('/home/ubuntu/environment/ecommerce/media/random.jpg', 'rb').read(),
                                          content_type='image/jpeg')
        self.shirt.save()
        
    def test_item_detail_get_success(self):
        response = self.client.get('/shoppingcart/product/random-slug/')
        self.assertTemplateUsed(response, 'shoppingcart/product.html')

    def test_add_to_cart_success_no_order(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        response = self.client.get('/shoppingcart/add_to_cart/random-slug/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'This item was added to your cart.')
        self.assertRedirects(response, '/shoppingcart/order_summary/')
    
    def test_update_cart_success_order_and_order_item_exist(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        orderitem = OrderItem(user=self.user, ordered=False, item=self.shirt, quantity=1)
        orderitem.save()
        order = Order(id=1, user=self.user, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        order.items.add(orderitem)
        order.save()
        response = self.client.get('/shoppingcart/add_to_cart/random-slug/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'This item quantity was updated.')
        self.assertRedirects(response, '/shoppingcart/order_summary/')
    
    def test_update_cart_success_order_exists_no_order_item(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        order = Order(id=1, user=self.user, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.get('/shoppingcart/add_to_cart/random-slug/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'This item was added to your cart.')
        self.assertRedirects(response, '/shoppingcart/order_summary/')
     
    def test_remove_from_cart_fail_no_active_order(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        response = self.client.get('/shoppingcart/remove_from_cart/random-slug/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You do not have an active order.')
        self.assertRedirects(response, '/shoppingcart/product/random-slug/')
        
    def test_remove_from_cart_fail_item_not_in_cart(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        order = Order(id=1, user=self.user, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.get('/shoppingcart/remove_from_cart/random-slug/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'This item is not in your cart.')
        self.assertRedirects(response, '/shoppingcart/product/random-slug/')
        
    def test_remove_from_cart_success(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        orderitem = OrderItem(user=self.user, ordered=False, item=self.shirt, quantity=1)
        orderitem.save()
        order = Order(id=1, user=self.user, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        order.items.add(orderitem)
        order.save()
        response = self.client.get('/shoppingcart/remove_from_cart/random-slug/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'This item was removed from your cart.')
        self.assertRedirects(response, '/shoppingcart/order_summary/')
     
    def test_remove_single_item_from_cart_fail_no_active_order(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        response = self.client.get('/shoppingcart/remove_single_item_from_cart/random-slug/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You do not have an active order.')
        self.assertRedirects(response, '/shoppingcart/product/random-slug/')
        
    def test_remove_single_item_from_cart_fail_item_not_in_cart(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        order = Order(id=1, user=self.user, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.get('/shoppingcart/remove_single_item_from_cart/random-slug/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'This item is not in your cart.')
        self.assertRedirects(response, '/shoppingcart/product/random-slug/')
        
    def test_remove_single_item_from_cart_success_quantity_more_than_1(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        orderitem = OrderItem(user=self.user, ordered=False, item=self.shirt, quantity=2)
        orderitem.save()
        order = Order(id=1, user=self.user, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        order.items.add(orderitem)
        order.save()
        response = self.client.get('/shoppingcart/remove_single_item_from_cart/random-slug/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'This item quantity was updated.')
        self.assertRedirects(response, '/shoppingcart/order_summary/')
        
    def test_remove_single_item_from_cart_success_quantity_equals_1(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        request = self.factory.get('/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        orderitem = OrderItem(user=self.user, ordered=False, item=self.shirt, quantity=1)
        orderitem.save()
        order = Order(id=1, user=self.user, 
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        order.items.add(orderitem)
        order.save()
        response = self.client.get('/shoppingcart/remove_single_item_from_cart/random-slug/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'This item was removed from your cart.')
        self.assertRedirects(response, '/shoppingcart/order_summary/')
        
class RequestRefundViewTest(TestCase):
    
    def setUp(self):
        self.credentials = {
            'username': 'User3457',
            'password': 'randompassword678'}
        self.user = User.objects.create_user(**self.credentials)
        self.user.save()
        self.refund_form1 = {
            'ref_code': 'test_order',
            'message': 'I want my money back!!!!',
            'email': 'newuser@yahoo.com'
        }
        self.refund_form2 = {
            'ref_code': 'invalid_ref_code',
            'message': 'I want my money back!!!!',
            'email': 'newuser@yahoo.com'
        }
    
    def test_request_refund_view_get_success(self):
        response = self.client.get('/shoppingcart/request_refund/')
        self.assertTemplateUsed(response, 'shoppingcart/request_refund.html')
        
    def test_request_refund_post_success(self):
        order = Order(id=1, user=self.user, ref_code='test_order',
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.post('/shoppingcart/request_refund/', self.refund_form1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your refund request was received.')
        self.assertRedirects(response, '/shoppingcart/request_refund/')
        
    def test_request_refund_post_fail(self):
        order = Order(id=1, user=self.user, ref_code='test_order',
                      ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC),
                      ordered=False)
        order.save()
        response = self.client.post('/shoppingcart/request_refund/', self.refund_form2)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'This order does not exist. Please check your email for the correct reference code.')
        self.assertRedirects(response, '/shoppingcart/request_refund/')
