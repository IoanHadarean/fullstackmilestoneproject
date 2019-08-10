from django.urls import path
from accounts.views import logout, login, registration, profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
]
