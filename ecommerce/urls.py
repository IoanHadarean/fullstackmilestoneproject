"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from shoppingcart import urls as cart_urls
from forum import views
import forum

urlpatterns = [
    path('', cart_urls.HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('forum/', include('forum.urls')),
    path('accounts/', include('accounts.urls')),
    path('reset/', include('accounts.urls_reset')),
    path('shoppingcart/', include('shoppingcart.urls')),
    path('contact/', include('contact.urls')),
    path('charts/data/', include('charts.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
