from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/(?P<pk>\d+)', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/(?P<pk>\d+)/edit', views.PostUpdateView.as_view(), name='post_edit'),
]