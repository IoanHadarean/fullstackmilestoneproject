from django.urls import path
from .views import (
    ItemDetailView, 
    CheckoutView, 
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart
)

urlpatterns = [
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', CheckoutView, name='checkout'),
    path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('home/', HomeView.as_view(), name='home'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart, 
         name='remove_single_item_from_cart'),
]