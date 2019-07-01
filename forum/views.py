from django.shortcuts import render
from forum.models import Post, Comment
from django.utils import timezone
from django.urls import reverse_lazy
from forum.forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)


class PostListView(ListView):
    """A class that defines the view for all the posts"""
    model = Post
    
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now().order_by('-published_date'))

class PostDetailView(DetailView):
    """A detail view for a single post"""
    model = Post
    
class CreatePostView(LoginRequiredMixin, CreateView):
    """
    Create a post and redirect to the details for
    that post. The user needs to be logged in to create a post.
    """
    login_url = 'accounts/login/'
    redirect_field_name = 'forum/post_detail.html'
    form_class = PostForm
    model = Post
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update a single post and redirect to the details for
    that post. The user needs to be logged in to update a post.
    """
    login_url = 'accounts/login/'
    redirect_field_name = 'forum/post_detail.html'
    form_class = PostForm
    model = Post
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a post and redirect to all posts"""
    model = Post
    success_url = reverse_lazy('post_list')
    
class DraftListView(LoginRequiredMixin, ListView):
    """Create a draft for a post"""
    login_url = 'accounts/login/'
    redirect_field_name = 'forum/post_list.html'
    model = Post