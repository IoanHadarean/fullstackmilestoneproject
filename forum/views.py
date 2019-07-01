from django.shortcuts import render
from forum.models import Post, Comment
from django.utils import timezone
from django.views.generic import (ListView, DetailView, CreateView)


class PostListView(ListView):
    """A class that defines the view for all the posts"""
    model = Post
    
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now().order_by('-published_date'))

class PostDetailView(DetailView):
    """A detail view for a single post"""
    model = Post
    

    