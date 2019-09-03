from django.test import TestCase
import datetime
import pytz
from datetime import date
from .views import day_orders, month_orders, last_3_months_orders, last_3_months_sales, last_3_days_sales, last_3_days_orders
from shoppingcart.models import Order
from django.contrib.auth.models import User


"""Get all orders and a date for testing"""
today_str = '08/25/19'
today_object = datetime.datetime.strptime(today_str, '%m/%d/%y')
today_date = today_object.utcnow().date()
orders = Order.objects.filter(ordered=True)


class TestCharts(TestCase):
    """Class for testing charts app"""

    """Set up the user and test orders for mocking the orders and sales"""
    def setUp(self):
        user = User.objects.create_user({'username': 'PepeMoeira', 'password': '999PepeHands'})
        user.save()
        order = Order(user=user, amount=500, ordered_date=datetime.datetime(2019, 8, 24, tzinfo=pytz.UTC))
        order.save()
        order = Order(user=user, amount=500, ordered_date=datetime.datetime(2019, 8, 25, tzinfo=pytz.UTC))
        order.save()
        order = Order(user=user, amount=500, ordered_date=datetime.datetime(2019, 7, 25, tzinfo=pytz.UTC))
        order.save()
        self.orders = Order.objects.all()

    """Test get charts view"""
    def test_charts_view(self):
        response = self.client.get('/charts/')
        self.assertTemplateUsed(response, 'charts/charts.html')
        self.assertEquals(response.status_code, 200)

    """Test each day orders (containing duplicates)"""
    def test_day_orders(self):
        daily_orders, last_3_days, orders_last_3_days_total, sales_last_3_days_total = day_orders(self.orders, datetime.date(2019, 8, 25))
        self.assertEqual(last_3_days, [datetime.date(2019, 8, 25), datetime.date(2019, 8, 24), datetime.date(2019, 8, 23)])
        self.assertEqual(daily_orders, [{'Sunday': 0}, {'Saturday': 1}, {'Friday': 0}, {'Sunday': 1}, {'Saturday': 0}, {'Friday': 0}])
        self.assertEqual(orders_last_3_days_total, 2)
        self.assertEqual(sales_last_3_days_total, 1000)

    """Test each month orders (containing duplicates)"""
    def test_month_orders(self):
        monthly_orders, last_3_months_datetime, orders_last_3_months_total, sales_last_3_months_total = month_orders(self.orders, datetime.date(2019, 8, 25))
        self.assertEqual(monthly_orders, [{'August': 1}, {'July': 0}, {'June': 0}, {'August': 1}, {'July': 0}, {'June': 0}, {'August': 0}, {'July': 1}, {'June': 0}])
        self.assertEqual(last_3_months_datetime, [datetime.date(2019, 8, 25), datetime.date(2019, 7, 26), datetime.date(2019, 6, 26)])
        self.assertEqual(orders_last_3_months_total, 3)
        self.assertEqual(sales_last_3_months_total, 1500)

    """Test last 3 days orders + total orders (no duplicates)"""
    def test_last_3_days_orders(self):
        orders_last_3_days = last_3_days_orders(self.orders, datetime.date(2019, 8, 25))
        self.assertEqual(orders_last_3_days, [{'Sunday': 1}, {'Saturday': 1}, {'Friday': 0}, {'Total': 2}])

    """Test last 3 months orders + total orders (no duplicates)"""
    def test_last_3_months_orders(self):
        orders_last_3_months = last_3_months_orders(self.orders, datetime.date(2019, 8, 25))
        self.assertEqual(orders_last_3_months, [{'August': 2}, {'July': 1}, {'June': 0}, {'Total': 3}])

    """Test last 3 days sales + total sales"""
    def test_last_3_days_sales(self):
        sales_last_3_days = last_3_days_sales(self.orders, datetime.date(2019, 8, 25))
        self.assertEqual(sales_last_3_days, [{'Sunday': 500}, {'Saturday': 500}, {'Friday': 0}, {'Total': 1000}])

    """Test last 3 months sales + total sales"""
    def test_last_3_months_sales(self):
        sales_last_3_months = last_3_months_sales(self.orders, datetime.date(2019, 8, 25))
        self.assertEqual(sales_last_3_months, [{'August': 1000}, {'July': 500}, {'June': 0}, {'Total': 1500}])

    """Test getting the data for creating the charts"""
    def test_get_data(self):
        response = self.client.post('/charts/data/')
        self.assertEqual(response.status_code, 200)
