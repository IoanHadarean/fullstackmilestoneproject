from django.urls import path
from .views import (
    ItemDetailView, 
    checkout, 
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart
)

urlpatterns = [
    path('product/<slug>', ItemDetailView.as_view(), name='product'),
    path('checkout/', checkout, name='checkout'),
    path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('home/', HomeView.as_view(), name='home'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>', remove_from_cart, name='remove_from_cart'),
]