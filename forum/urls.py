from django.urls import path, re_path, include
from . import views
from search import urls as urls_search

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('user/<str:username>/', views.UserPostListView.as_view(), name='user_posts'),
    re_path(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    path('posts/new/', views.CreatePostView.as_view(), name='post_new'),
    re_path(r'^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='post_edit'),
    re_path(r'^post/(?P<pk>\d+)/remove/$', views.PostDeleteView.as_view(), name='post_remove'),
    path('drafts/<str:username>/', views.DraftListView.as_view(), name='post_draft_list'),
    re_path(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    re_path(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    re_path(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    re_path(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    path('like/', views.like_post, name='like_post'),
    path('', include(urls_search)),
]