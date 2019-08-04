from django.shortcuts import render
from django.http import JsonResponse
from datetime import date
import datetime
from shoppingcart.models import Order
from django.views.generic import View


class ChartsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts/charts.html', {})

def recursive(order, monthly_orders, months, month, orders_month, i):
    for o in monthly_orders:
        index = i
        while index < len(months):
        if months[i] in list(order.keys())[0]:
            orders_month += order[months[i]]
            month.update({months[i]: orders_month})
            del order[months[i]]

def get_data(request, *args, **kwargs):
    orders = Order.objects.filter(ordered=True)
    today = date.today()
    
    data = {
        'orders_last_5_days': 0,
        'orders_last_3_months': 0,
        'orders_per_day_list': [],
        'orders_per_month_list': [],
        'sales_last_5_days': 0,
        'sales_last_3_months': 0,
    }
    
    last_5_days = []
    for i in range(0, 5):
        last_5_days.append(today - datetime.timedelta(i))
        
    last_3_months = []
    last_3_months_datetime = []
    for i in range(0, 3):
        last_3_months.append((today - datetime.timedelta(i * 365/12)).month)
        last_3_months_datetime.append(today - datetime.timedelta(i * 365/12))
    
    daily_orders = []
    monthly_orders = []
    for order in orders:
        if order.ordered_date.date() in last_5_days:
            data['orders_last_5_days'] += 1
            data['sales_last_5_days'] += order.get_total()
            for date_time in last_5_days:
                orders_per_day = 0
                if order.ordered_date.date() == date_time:
                    orders_per_day += 1
                    daily_orders.append({date_time.strftime("%A") : orders_per_day})
                else:
                    daily_orders.append({date_time.strftime("%A") : 0})
        if order.ordered_date.date().month in last_3_months:
            data['orders_last_3_months'] += 1
            data['sales_last_3_months'] += order.get_total()
            for date_time in last_3_months_datetime:
                orders_per_month = 0
                if order.ordered_date.date().month == date_time.month:
                    orders_per_month += 1
                    monthly_orders.append({date_time.strftime("%B"): orders_per_month})
                else:
                    monthly_orders.append({date_time.strftime("%B"): orders_per_month})
  
    months = []
    for order in monthly_orders:
        if list(order.keys())[0] not in months:
            months.append(list(order.keys())[0])
            
    first_month = {}
    second_month = {}
    third_month = {}
    orders_first_month = 0
    orders_second_month = 0
    orders_third_month = 0
    for order in monthly_orders:
        i = 0
        while i < len(months):
            month = {}
            orders_month = 0
            if months[i] in list(order.keys())[0]:
                orders_month += order[months[i]]
                month.update({months[i]: orders_month})
                del order[months[i]]
                recursive(order, monthly_orders, months, month, orders_month, i)
            else:
                data['orders_per_month_list'].append(month)
                i += 1
        
    
    days = []
    for order in daily_orders:
        if list(order.keys())[0] not in days:
            days.append(list(order.keys())[0])
            
    first_day = {}
    second_day = {}
    third_day = {}
    fourth_day = {}
    fifth_day = {}
    orders_first_day = 0
    orders_second_day = 0
    orders_third_day = 0
    orders_fourth_day = 0
    orders_fifth_day = 0

    
    
    
    return JsonResponse(data)
        