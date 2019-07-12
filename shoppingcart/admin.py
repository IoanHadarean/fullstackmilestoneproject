from django.contrib import admin
from shoppingcart.models import Item, OrderItem, Order, BillingAddress, Payment

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BillingAddress)
admin.site.register(Payment)
