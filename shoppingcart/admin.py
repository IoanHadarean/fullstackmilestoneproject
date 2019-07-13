from django.contrib import admin
from shoppingcart.models import Item, OrderItem, Order, Payment, Coupon, Refund 

"""Change the order from refund requested to refund granted"""
def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

"""Change the order status to being delivered"""
def order_being_delivered(modeladmin, request, queryset):
    queryset.update(being_delivered=True)
    
"""Change the order status to received"""
def order_received(modeladmin, request, queryset):
    queryset.update(being_delivered=False, received=True)

"""Add descriptions for admin commands"""
make_refund_accepted.short_description = 'Update order to refund granted'
order_being_delivered.short_description = 'Update order to order being delivered'
order_received.short_description = 'Update order to order received'


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
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted, 
               order_being_delivered,
               order_received]
    
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
