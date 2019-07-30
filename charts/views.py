from django.shortcuts import render
from django.http import JsonResponse
from datetime import date
import datetime
from shoppingcart.models import Order

def get_data(request, *args, **kwargs):
    orders = Order.objects.filter(ordered=True)
    today = date.today()
    
    data = {
        'orders_today': 0,
        'orders_last_7_days': 0,
        'orders_this_month': 0,
        'orders_last_3_months': 0,
        'orders_last_6_months': 0,
        'orders_this_year': 0,
        'sales_today': 0,
        'sales_last_7_days': 0,
        'sales_this_month': 0,
        'sales_last_3_months': 0,
        'sales_last_6_months': 0,
        'sales_this_year': 0
    }
    
    last_7_days = []
    for i in range(0, 7):
        last_7_days.append(today - datetime.timedelta(i))
        
    last_3_months = []
    for i in range(0, 3):
        last_3_months.append((today - datetime.timedelta(i * 365/12)).month)
        
    last_6_months = []
    for i in range(0, 6):
        last_6_months.append((today - datetime.timedelta(i * 365/12)).month)
    
    for order in orders:
        print(order.ordered_date)
        if order.ordered_date.date() == today:
            data['orders_today'] += 1
            data['sales_today'] += order.get_total()
        if order.ordered_date.month == today.month:
            data['orders_this_month'] += 1
            data['sales_this_month'] += order.get_total()
        if order.ordered_date.year == today.year:
            data['orders_this_year'] += 1
            data['sales_this_year'] += order.get_total() 
        if order.ordered_date.date() in last_7_days:
            data['orders_last_7_days'] += 1
            data['sales_last_7_days'] += order.get_total()
        if order.ordered_date.date().month in last_3_months:
            data['orders_last_3_months'] += 1
            data['sales_last_3_months'] += order.get_total()
        if order.ordered_date.date().month in last_6_months:
            data['orders_last_6_months'] += 1
            data['sales_last_6_months'] += order.get_total()
    return JsonResponse(data)
        