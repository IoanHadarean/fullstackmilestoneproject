from django.shortcuts import render
from django.http import JsonResponse
from datetime import date
import datetime
from shoppingcart.models import Order
from django.views.generic import View

orders = Order.objects.filter(ordered=True)
today = date.today()


class ChartsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts/charts.html', {})
        
        
def day_orders():
    last_3_days = []
    for i in range(0, 3):
        last_3_days.append(today - datetime.timedelta(i))
    
    daily_orders = []
    orders_last_3_days_total = 0
    sales_last_3_days_total = 0
    for order in orders:
        if order.ordered_date.date() in last_3_days:
            orders_last_3_days_total += 1
            sales_last_3_days_total += order.amount
            for date_time in last_3_days:
                orders_per_day = 0
                if order.ordered_date.date() == date_time:
                    orders_per_day += 1
                    daily_orders.append({date_time.strftime("%A") : orders_per_day})
                else:
                    daily_orders.append({date_time.strftime("%A") : 0})

                    
    return daily_orders, last_3_days, orders_last_3_days_total, sales_last_3_days_total
    

def month_orders():
    last_3_months = []
    last_3_months_datetime = []
    for i in range(0, 3):
        last_3_months.append((today - datetime.timedelta(i * 365/12)).month)
        last_3_months_datetime.append(today - datetime.timedelta(i * 365/12))
        
        
    monthly_orders = []
    orders_last_3_months_total = 0
    sales_last_3_months_total = 0
    for order in orders:
        if order.ordered_date.date().month in last_3_months:
            orders_last_3_months_total += 1
            sales_last_3_months_total += order.amount
            for date_time in last_3_months_datetime:
                orders_per_month = 0
                if order.ordered_date.date().month == date_time.month:
                    orders_per_month += 1
                    monthly_orders.append({date_time.strftime("%B"): orders_per_month})
                else:
                    monthly_orders.append({date_time.strftime("%B"): orders_per_month})
                    
    return monthly_orders, last_3_months_datetime, orders_last_3_months_total, sales_last_3_months_total
    

def last_3_days_orders():
    
    daily_orders, last_3_days, orders_last_3_days_total, sales_last_3_days_total = day_orders()

    days = []
    for date in last_3_days:
        days.append(date.strftime("%A"))
            
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
            
    if first_day == {}:
        first_day.update({days[0]: 0})
    if second_day == {}:
        second_day.update({days[1]: 0})
    if third_day == {}:
        third_day.update({days[2]: 0})
            
    orders_last_3_days = []
    orders_last_3_days.append(first_day)
    orders_last_3_days.append(second_day)
    orders_last_3_days.append(third_day)
    orders_last_3_days.append({'Total': orders_last_3_days_total})
    
    return orders_last_3_days


def last_3_months_orders():
    
    monthly_orders, last_3_months_datetime, orders_last_3_months_total, sales_last_3_months_total = month_orders()
    
    months = []
    for date in last_3_months_datetime:
        months.append(date.strftime("%B"))
            
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
            
    if first_month == {}:
        first_month.update({months[0]: 0})
    if second_month == {}:
        second_month.update({months[1]: 0})
    if third_month == {}:
        third_month.update({months[2]: 0})
            
    orders_last_3_months = []
    orders_last_3_months.append(first_month)
    orders_last_3_months.append(second_month)
    orders_last_3_months.append(third_month)
    orders_last_3_months.append({'Total': orders_last_3_months_total})
    
    return orders_last_3_months
        
        
def last_3_days_sales():

    daily_orders, last_3_days, orders_last_3_days_total, sales_last_3_days_total = day_orders()

    days = []
    for date in last_3_days:
        days.append(date.strftime("%A"))
            
    first_day = {}
    second_day = {}
    third_day = {}
    sales_first_day = 0
    sales_second_day = 0
    sales_third_day = 0
    for order in orders:
        if days[0] == order.ordered_date.date().strftime("%A"):
            sales_first_day += order.amount
            first_day.update({days[0]: sales_first_day})
        elif days[1] == order.ordered_date.date().strftime("%A"):
            sales_second_day += order.amount
            second_day.update({days[1]: sales_second_day})
        elif days[2] == order.ordered_date.date().strftime("%A"):
            sales_third_day += order.amount
            third_day.update({days[2]: sales_third_day})
            
    if first_day == {}:
        first_day.update({days[0]: 0})
    if second_day == {}:
        second_day.update({days[1]: 0})
    if third_day == {}:
        third_day.update({days[2]: 0})
            
    sales_last_3_days = []
    sales_last_3_days.append(first_day)
    sales_last_3_days.append(second_day)
    sales_last_3_days.append(third_day)
    sales_last_3_days.append({'Total': sales_last_3_days_total})
    
    return sales_last_3_days
        
        
def last_3_months_sales():
    
    monthly_orders, last_3_months_datetime, orders_last_3_months_total, sales_last_3_months_total = month_orders()
    
    months = []
    for date in last_3_months_datetime:
        months.append(date.strftime("%B"))
            
    first_month = {}
    second_month = {}
    third_month = {}
    sales_first_month = 0
    sales_second_month = 0
    sales_third_month = 0
    
    for order in orders:
        if months[0] == order.ordered_date.date().strftime("%B"):
            sales_first_month += order.amount
            first_month.update({months[0]: sales_first_month})
        elif months[1] == order.ordered_date.date().strftime("%B"):
            sales_second_month += order.amount
            second_month.update({months[1]: sales_second_month})
        elif months[2] == order.ordered_date.date().strftime("%B"):
            sales_third_month += order.amount
            third_month.update({months[2]: sales_third_month})
            
    if first_month == {}:
        first_month.update({months[0]: 0})
    if second_month == {}:
        second_month.update({months[1]: 0})
    if third_month == {}:
        third_month.update({months[2]: 0})
            
    sales_last_3_months = []
    sales_last_3_months.append(first_month)
    sales_last_3_months.append(second_month)
    sales_last_3_months.append(third_month)
    sales_last_3_months.append({'Total': sales_last_3_months_total})
    
    return sales_last_3_months
    
    
def get_data(request, *args, **kwargs):
    
    orders_last_3_days = last_3_days_orders()
    orders_last_3_months = last_3_months_orders()
    sales_last_3_days = last_3_days_sales()
    sales_last_3_months = last_3_months_sales()
    
    data = {
        'orders_last_3_days': orders_last_3_days,
        'orders_last_3_months': orders_last_3_months,
        'sales_last_3_days': sales_last_3_days,
        'sales_last_3_months': sales_last_3_months,
    }
    
    return JsonResponse(data)
        