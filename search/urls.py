from django.urls import path
from . import views

urlpatterns = [
    path('products_results/<search_text>/', views.products_results, name='products_results'),
    path('search_products/', views.search_products, name='search_products'),
    path('filter_by_tags/<category>/', views.filter_by_tags, name='filter_by_tags'),
]
