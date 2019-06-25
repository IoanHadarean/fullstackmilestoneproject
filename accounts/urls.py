from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('register/', views.registration, name='registration'),
    path('profile/', views.user_profile, name='profile'),
]