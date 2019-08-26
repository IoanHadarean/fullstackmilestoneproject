from django.test import TestCase
import datetime
import pytz
from datetime import date
from django.test.client import Client
from .views import day_orders, month_orders, last_3_months_orders, last_3_months_sales, last_3_days_sales, last_3_days_orders
from shoppingcart.models import Order
from django.contrib.auth.models import User


today_str = '08/25/19'
today_object = datetime.datetime.strptime(today_str, '%m/%d/%y')
today = today_object.utcnow().date()
orders = Order.objects.filter(ordered=True)


class TestChartsDayOrders(TestCase):
    
    def setUp(self):
        user = User.objects.create_user({'username': 'PepeMoeira', 'password':'999PepeHands'})
        user.save()
        order = Order(user=user, amount=500, ordered_date=datetime.datetime(2019, 8, 24, tzinfo=pytz.UTC))
        order.save()
        order = Order(user=user, amount=500, ordered_date=datetime.datetime(2019, 8, 25, tzinfo=pytz.UTC))
        order.save()
        order = Order(user=user, amount=500, ordered_date=datetime.datetime(2019, 7, 25, tzinfo=pytz.UTC))
        order.save()
        self.orders = Order.objects.all()
        
    def test_charts_view(self):
        client = Client()
        response = client.get('/charts/')
        self.assertTemplateUsed(response, 'charts/charts.html')
        self.assertEquals(response.status_code, 200)
    
    def test_day_orders(self):
        daily_orders, last_3_days, orders_last_3_days_total, sales_last_3_days_total = day_orders(today, self.orders)
        self.assertEqual(last_3_days, [today - datetime.timedelta(0), today - datetime.timedelta(1), today - datetime.timedelta(2)])
        self.assertEqual(daily_orders, [{'Monday': 0}, {'Sunday': 0}, {'Saturday': 1}, {'Monday': 0}, {'Sunday': 1}, {'Saturday': 0}])
        self.assertEqual(orders_last_3_days_total, 2)
        self.assertEqual(sales_last_3_days_total, 1000)
        
    def test_month_orders(self):
        monthly_orders, last_3_months_datetime, orders_last_3_months_total, sales_last_3_months_total = month_orders(today, self.orders)
        self.assertEqual(monthly_orders, [{'August': 1}, {'July': 0}, {'June': 0}, {'August': 1}, {'July': 0}, {'June': 0}, {'August': 0}, {'July': 1}, {'June': 0}])
        self.assertEqual(last_3_months_datetime, [datetime.date(2019, 8, 26), datetime.date(2019, 7, 27), datetime.date(2019, 6, 27)])
        self.assertEqual(orders_last_3_months_total, 3)
        self.assertEqual(sales_last_3_months_total, 1500)
        
    def test_last_3_days_orders(self):
        orders_last_3_days = last_3_days_orders(today, self.orders)
        self.assertEqual(orders_last_3_days, [{'Monday': 0}, {'Sunday': 1}, {'Saturday': 1}, {'Total': 2}])
        
    def test_last_3_months_orders(self):
        orders_last_3_months = last_3_months_orders(today, self.orders)
        self.assertEqual(orders_last_3_months, [{'August': 2}, {'July': 1}, {'June': 0}, {'Total': 3}])
        
    def test_last_3_days_sales(self):
        sales_last_3_days = last_3_days_sales(today, self.orders)
        self.assertEqual(sales_last_3_days, [{'Monday': 0}, {'Sunday': 500}, {'Saturday': 500}, {'Total': 1000}])
        
    def test_last_3_months_sales(self):
        sales_last_3_months = last_3_months_sales(today, self.orders)
        self.assertEqual(sales_last_3_months, [{'August': 1000}, {'July': 500}, {'June': 0}, {'Total': 1500}])
        
    def test_get_data(self):
        response = self.client.post('/charts/data/')
        self.assertEqual(response.status_code, 200)
        
        
        
        
        
        
        