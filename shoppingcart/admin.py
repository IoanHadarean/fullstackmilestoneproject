from django.contrib import admin
from shoppingcart.models import Item, OrderItem, Order, Payment, Coupon

class OrderAdmin(admin.ModelAdmin):
    """
    Added order display by user and ordered 
    into the admin page
    """
    list_display = ['user', 
                    'ordered', 
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'billing_address',
                    'payment',
                    'coupon'
                   ]
    list_display_links = [
        'user',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered', 
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted'
                  ]
    
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
