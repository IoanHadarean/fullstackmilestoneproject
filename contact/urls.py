from django.urls import path, re_path, include
from .views import ContactView

urlpatterns = [
    path('', ContactView.as_view(), name='contact'),
    ]