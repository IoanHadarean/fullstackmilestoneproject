from django.contrib import admin
from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Address, UserCoupon


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
    Custom order admin display, including search
    and filters.
    """
    list_display = [
                    'user', 
                    'ordered', 
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'billing_address',
                    'shipping_address',
                    'payment',
                    'coupon'
                   ]
    list_display_links = [
        'user',
        'billing_address',
        'shipping_address',
        'payment',
        'coupon'
    ]
    list_filter = [
                   'ordered', 
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted'
                  ]
    search_fields = [
                     'user__username',
                     'ref_code'
                    ]
    actions = [
               make_refund_accepted, 
               order_being_delivered,
               order_received
              ]
               

class AddressAdmin(admin.ModelAdmin):
    """
    Custom address admin display, including search 
    and filters.
    """
    list_display = [
                    'user',
                    'street_address',
                    'appartment_address',
                    'country',
                    'zip_code',
                    'address_type',
                    'default'
                   ]
    list_filter = [
                   'default',
                   'address_type',
                   'country'
                  ]
    search_fields = [
                     'user',
                     'street_address',
                     'appartment_address',
                     'zip_code'
                    ]
admin.site.unregister(Item)
admin.site.unregister(OrderItem)
admin.site.unregister(Order)
admin.site.unregister(Payment)
admin.site.unregister(Coupon)
admin.site.unregister(Refund)
admin.site.unregister(Address)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(UserCoupon)
admin.site.register(Address, AddressAdmin)


