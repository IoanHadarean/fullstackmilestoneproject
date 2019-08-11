from django.urls import path
from .views import get_data, ChartsView

urlpatterns = [
    path('charts/data/', get_data, name='chart-data'),
    path('charts/', ChartsView.as_view(), name='charts')
]
