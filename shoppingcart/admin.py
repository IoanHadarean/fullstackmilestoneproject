from django.contrib import admin
from shoppingcart.models import Item, OrderItem, Order, Payment, Coupon

class OrderAdmin(admin.ModelAdmin):
    """
    Added order display by user and ordered 
    into the admin page
    """
    list_display = ['user', 'ordered']
    
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
