from django.shortcuts import render
from django.http import JsonResponse
from datetime import date
import datetime
from shoppingcart.models import Order
from django.views.generic import View


class ChartsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts/charts.html', {})

def get_data(request, *args, **kwargs):
    orders = Order.objects.filter(ordered=True)
    today = date.today()
    
    data = {
        'orders_last_7_days': 0,
        'orders_last_3_months': 0,
        'orders_per_day': [],
        'orders_per_day_dict': {},
        'orders_per_day_unique': {},
        'orders_per_month': [],
        'sales_last_7_days': 0,
        'sales_last_3_months': 0,
    }
    
    last_7_days = []
    for i in range(0, 7):
        last_7_days.append(today - datetime.timedelta(i))
        
    print(last_7_days[1].strftime("%A"))
        
    last_3_months = []
    for i in range(0, 3):
        last_3_months.append((today - datetime.timedelta(i * 365/12)).month)
    
    for order in orders:
        if order.ordered_date.date() in last_7_days:
            data['orders_last_7_days'] += 1
            data['sales_last_7_days'] += order.get_total()
            for date_time in last_7_days:
                orders_per_day = 0
                if order.ordered_date.date() == date_time:
                    orders_per_day += 1
                    data['orders_per_day'].append({date_time.strftime("%A") : orders_per_day})
                else:
                    data['orders_per_day'].append({date_time.strftime("%A") : 0})
        if order.ordered_date.date().month in last_3_months:
            data['orders_last_3_months'] += 1
            data['sales_last_3_months'] += order.get_total()
    
    print(data['orders_per_day'])
    
    def update_without_overwriting(d, x):
        d.update({k: v for k, v in x.items() if v > 0 | (v )})
    
    
    for i in range(0, len(data['orders_per_day'])):
        update_without_overwriting(data['orders_per_day_dict'], data['orders_per_day'][i])
    
    print(data['orders_per_day_dict'])
    
    i = 0
    while i < len(list(data['orders_per_day'].keys())):
        index_key = list(data['orders_per_day'].keys())[i]
        for k, v in data['orders_per_day'].items():
            if k == index_key:
                if data['orders_per_day'][k] > data['orders_per_day'].get(index_key) :
                    data['orders_per_day_unique'][k] = v
                    i += 1
                elif data['orders_per_day'][k] == data['orders_per_day'].get(index_key):
                    data['orders_per_day_unique'][k] = v
                    i += 1
                elif data['orders_per_day'][k] < data['orders_per_day'].get(index_key):
                    data['orders_per_day_unique'][index_key] = data['orders_per_day'].get(index_key)
                    i += 1
    return JsonResponse(data)
        