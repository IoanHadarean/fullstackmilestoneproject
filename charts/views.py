from django.shortcuts import render
from django.http import JsonResponse
from datetime import date
from shoppingcart.models import Order

def get_data(request, *args, **kwargs):
    orders = Order.objects.filter(ordered=True)
    today = date.today()
    
    data = {
        'orders_by_today': 0,
        'orders_by_week': 0,
        'orders_by_month': 0
    }
    
    for order in orders:
        if order.created_date == today:
            data['orders_by_today'] += 1
            print(data['orders_by_today'])
    return JsonResponse(data)
