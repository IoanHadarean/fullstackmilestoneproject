from django.urls import path
from .views import (
    ItemDetailView, 
    checkout, 
    HomeView, 
    add_to_cart
)

urlpatterns = [
    path('product/<slug>', ItemDetailView.as_view(), name='product'),
    path('checkout/', checkout, name='checkout'),
    path('home/', HomeView.as_view(), name='home'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
]