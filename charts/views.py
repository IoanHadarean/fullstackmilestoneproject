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
        'orders_last_3_days': [],
        'orders_last_3_months': [],
        'sales_last_3_days': [],
        'sales_last_3_months': [],
    }
    
    last_3_days = []
    for i in range(0, 3):
        last_3_days.append(today - datetime.timedelta(i))
        
    last_3_months = []
    last_3_months_datetime = []
    for i in range(0, 3):
        last_3_months.append((today - datetime.timedelta(i * 365/12)).month)
        last_3_months_datetime.append(today - datetime.timedelta(i * 365/12))
    
    daily_orders = []
    monthly_orders = []
    orders_last_3_days_total = 0
    sales_last_3_days_total = 0
    orders_last_3_months_total = 0
    sales_last_3_months_total = 0
    for order in orders:
        if order.ordered_date.date() in last_3_days:
            orders_last_3_days_total += 1
            sales_last_3_days_total += order.get_total()
            for date_time in last_3_days:
                orders_per_day = 0
                if order.ordered_date.date() == date_time:
                    orders_per_day += 1
                    daily_orders.append({date_time.strftime("%A") : orders_per_day})
                else:
                    daily_orders.append({date_time.strftime("%A") : 0})
        if order.ordered_date.date().month in last_3_months:
            orders_last_3_months_total += 1
            sales_last_3_months_total += order.get_total()
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
        if months[0] in list(order.keys())[0]:
            orders_first_month += order[months[0]]
            first_month.update({months[0]: orders_first_month})
        elif months[1] in list(order.keys())[0]:
            orders_second_month += order[months[1]]
            second_month.update({months[1]: orders_second_month})
        elif months[2] in list(order.keys())[0]:
            orders_third_month += order[months[2]]
            third_month.update({months[2]: orders_third_month})
            
        
    data['orders_last_3_months'].append(first_month)
    data['orders_last_3_months'].append(second_month)
    data['orders_last_3_months'].append(third_month)
    data['orders_last_3_months'].append({'Total': orders_last_3_months_total})
    
    days = []
    for order in daily_orders:
        if list(order.keys())[0] not in days:
            days.append(list(order.keys())[0])
            
    first_day = {}
    second_day = {}
    third_day = {}
    orders_first_day = 0
    orders_second_day = 0
    orders_third_day = 0
    for order in daily_orders:
        if days[0] in list(order.keys())[0]:
            orders_first_day += order[days[0]]
            first_day.update({days[0]: orders_first_day})
        elif days[1] in list(order.keys())[0]:
            orders_second_day += order[days[1]]
            second_day.update({days[1]: orders_second_day})
        elif days[2] in list(order.keys())[0]:
            orders_third_day += order[days[2]]
            third_day.update({days[2]: orders_third_day})
            
    data['orders_last_3_days'].append(first_day)
    data['orders_last_3_days'].append(second_day)
    data['orders_last_3_days'].append(third_day)
    data['orders_last_3_days'].append({'Total': orders_last_3_days_total})
    
    return JsonResponse(data)
        