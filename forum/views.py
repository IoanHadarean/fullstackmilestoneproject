from django.shortcuts import render, get_object_or_404, redirect
from forum.models import Post, Comment
from django.utils import timezone
from django.urls import reverse_lazy
from forum.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)


class PostListView(ListView):
    """A class that defines the view for all the posts"""
    model = Post
    
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    """A detail view for a single post"""
    model = Post
    
class CreatePostView(LoginRequiredMixin, CreateView):
    """
    Create a post and redirect to the details for
    that post. The user needs to be logged in to create a post.
    """
    login_url = 'accounts/login/'
    redirect_field_name = 'post_detail.html'
    form_class = PostForm
    model = Post
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update a single post and redirect to the details for
    that post. The user needs to be logged in to update a post.
    """
    login_url = '/login/'
    redirect_field_name = 'post_detail.html'
    form_class = PostForm
    model = Post
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a post and redirect to all posts"""
    model = Post
    success_url = reverse_lazy('post_list')
    
class DraftListView(LoginRequiredMixin, ListView):
    """Draft view for a post"""
    login_url = '/login/'
    redirect_field_name = 'post_list.html'
    model = Post
    
    def get_query_set(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')
        
        
#######################################
#######################################

@login_required
def post_publish(request,pk):
    """Allow publishing a post"""
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def add_comment_to_post(request,pk):
    """Allow adding a comment to a post"""
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form':form})
    
@login_required
def comment_approve(request):
    """Approve a post comment"""
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)
    
@login_required
def comment_remove(request,pk):
    """Delete a post comment"""
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)