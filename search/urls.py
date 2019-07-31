from django.urls import path
from . import views

urlpatterns = [
    path('search_results/<search_text>/', views.search_results, name='search_results'),
    path('search_products/', views.search_products, name='search_products'),
    path('filter/dresses/', views.filter_by_dresses, name='filter_by_dresses'),
    path('filter/shoes/', views.filter_by_shoes, name='filter_by_shoes'),
    path('filter/suits/', views.filter_by_suits, name='filter_by_suits'),
    path('filter/veils/', views.filter_by_veils, name='filter_by_veils'),
    path('filter/rings/', views.filter_by_rings, name='filter_by_rings'),
    path('filter/flowers/', views.filter_by_flowers, name='filter_by_flowers'),
    path('filter/hair_accessories/', views.filter_by_hair_accessories, name='filter_by_hair_accessories'),
    path('filter/purses/', views.filter_by_purses, name='filter_by_purses'),
    path('filter/shirts/', views.filter_by_shirts, name='filter_by_shirts'),
    path('filter/belts/', views.filter_by_belts, name='filter_by_belts'),
    path('filter_by_tags/<category>/', views.filter_by_tags, name='filter_by_tags'),
]
