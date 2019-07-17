from django.urls import path, include
from .views import (
    ItemDetailView, 
    CheckoutView, 
    HomeView,
    PaymentView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    AddCouponView,
    RequestRefundView
)
from search import urls as search_urls

urlpatterns = [
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('home/', HomeView.as_view(), name='home'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('add_coupon/', AddCouponView.as_view(), name='add_coupon'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart, 
         name='remove_single_item_from_cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request_refund/',RequestRefundView.as_view(), name='request_refund'),
    path('', include(search_urls))
]