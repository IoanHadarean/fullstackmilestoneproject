from django.urls import path, include
from .views import (
    CheckoutView,
    HomeView,
    PaymentView,
    OrderSummaryView,
    item_detail,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    delete_card,
    save_default_card,
    AddCouponView,
    RequestRefundView,
    UpdateCardView,
)
from search import urls as search_urls

urlpatterns = [
    path('product/<slug>/', item_detail , name='product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('home/', HomeView.as_view(), name='home'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('add_coupon/', AddCouponView.as_view(), name='add_coupon'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart,
         name='remove_single_item_from_cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('payment/delete_card/<id>/', delete_card, name='delete_card'),
    path('payment/save_default_card/<id>/', save_default_card, name='save_default_card'),
    path('request_refund/', RequestRefundView.as_view(), name='request_refund'),
    path('update_card/<id>/', UpdateCardView.as_view(), name='update_card'),
    path('', include(search_urls))
]
