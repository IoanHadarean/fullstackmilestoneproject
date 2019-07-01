from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/(?P<pk>\d+)', views.PostDetailView.as_view(), name='post_detail')
]