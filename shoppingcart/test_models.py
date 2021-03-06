from django.test import TestCase
from .models import Item, Address, Payment, Coupon, Refund, Order, OrderItem
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
import pytz


class TestShoppingCartModels(TestCase):
    """Class for testing shopping cart models"""

    """
    Set up the test item, test address, test payment,
    test coupon, test order item, test order and test refund
    """
    def setUp(self):
        self.item = Item(title='Shirt', price=300, discount_price=50, category='Shirts', label='primary', slug='random-slug', description='shirt')
        self.item.image = SimpleUploadedFile(name='BE266_rose_top.jpg',
                                             content=open('/home/ubuntu/environment/ecommerce/media/random.jpg', 'rb').read(),
                                             content_type='image/jpeg')
        self.item.save()
        user = User.objects.create_user('goagl', 'hello@yahoo.com', 'randompassword')
        user.save()
        self.address = Address(user=user, address_type='S')
        self.address.save()
        self.payment = Payment(user=user, amount=300)
        self.payment.save()
        self.coupon = Coupon(code='WEDDING', amount=200)
        self.coupon.save()
        self.orderitem = OrderItem(user=user, ordered=False, item=self.item, quantity=2)
        self.orderitem.save()
        self.order = Order(user=user, ordered_date=datetime.datetime(2019, 7, 26, tzinfo=pytz.UTC))
        self.order.save()
        self.refund = Refund(order=self.order, reason='I want my money back')
        self.refund.save()

    """Test item '__str__' and 'get_discount_price' methods"""
    def test_item_title_discount_price_and_final_price(self):
        self.assertEqual(str(self.item), 'Shirt')
        total_price = self.item.get_discount_price()
        self.assertEqual(total_price, 250)

    """Test '__str__' method of address, payment and order"""
    def test_address_order_and_payment_username(self):
        self.assertEqual(str(self.address), 'goagl')
        self.assertEqual(str(self.payment), 'goagl')
        self.assertEqual(str(self.order), 'goagl')

    """Test '__str__' method for coupon"""
    def test_coupon_code(self):
        self.assertEqual(str(self.coupon), 'WEDDING')

    """Test '__str__' method for refund"""
    def test_refund_pk(self):
        self.assertEqual(str(self.refund), "1")

    """Test '__str__' and 'get_final_price' methods of order item"""
    def test_order_item_quantity_of_item_and_final_price(self):
        self.assertEqual(str(self.orderitem), '2 of Shirt')
        self.assertEqual(self.orderitem.get_final_price(), 500)

    """Test 'get_total_item_discount_price' and 'get_amount_saved' methods of order item"""
    def test_order_item_total_discount_price_and_amount_saved(self):
        self.assertEqual(self.orderitem.get_total_item_discount_price(), 500)
        self.assertEqual(self.orderitem.get_amount_saved(), 100)
