from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/(?P<pk>\d+)', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/(?P<pk>\d+)/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/(?P<pk>\d+)/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]