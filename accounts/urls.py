from django.urls import path
from accounts.views import logout, login, registration, user_profile, index

urlpatterns = [
    path('index/', index, name='index'),
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', user_profile, name='profile'),
]