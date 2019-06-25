from django.urls import path
from accounts.views import logout, login, registration, user_profile, index
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/', index, name='index'),
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', user_profile, name='profile'),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
         name='password_reset_confirm'),
         
]