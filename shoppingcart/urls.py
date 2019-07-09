from django.urls import path
from .views import ItemDetailView, checkout, HomeView

urlpatterns = [
    path('product/<slug>', ItemDetailView.as_view(), name='product'),
    path('checkout/', checkout, name='checkout'),
    path('home/', HomeView.as_view(), name='home'),
]