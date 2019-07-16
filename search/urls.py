from django.urls import path
from . import views

urlpatterns = [
    path('search_posts/', views.search_posts, name='search_posts'),
    path('search_drafts/', views.search_drafts, name='search_drafts'),
    path('search_products/', views.search_products, name='search_products'),
    path('filter/dresses/<category>/', views.filter_by_dresses, name='filter_by_dresses'),
    path('filter/shoes/<category>/', views.filter_by_shoes, name='filter_by_shoes'),
    path('filter/suits/<category>/', views.filter_by_suits, name='filter_by_suits'),
    path('filter/veils/<category>/', views.filter_by_veils, name='filter_by_veils'),
    path('filter/rings/</category>/', views.filter_by_rings, name='filter_by_rings'),
    path('filter/flowers/</category>/', views.filter_by_flowers, name='filter_by_flowers'),
    path('filter/hair_accessories/<category>/', views.filter_by_hair_accessories, name='filter_by_hair_accessories'),
    path('filter/purses/<category>/', views.filter_by_purses, name='filter_by_purses'),
    path('filter/neckties/<category>/', views.filter_by_neckties, name='filter_by_neckties'),
    path('filter/shirts/<category>/', views.filter_by_shirts, name='filter_by_shirts'),
    path('filter/belts/<category>/', views.filter_by_belts, name='filter_by_belts'),
]
