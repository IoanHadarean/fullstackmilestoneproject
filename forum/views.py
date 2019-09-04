from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from forum.models import Post, Comment
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from forum.forms import PostForm, CommentForm, PostEditForm, CommentEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, CreateView,
                                  UpdateView, RedirectView, DeleteView)


class PostListView(ListView):
    """A class that defines the view for all the posts"""
    model = Post
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class UserPostListView(ListView):
    """A class that defines the view for a specific user's posts"""
    model = Post
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user, published_date__isnull=False).order_by('-published_date')


class CreatePostView(LoginRequiredMixin, CreateView):
    """
    Create a post and redirect to the details for
    that post. The user needs to be logged in to create a post.
    """
    def get(self, *args, **kwargs):
        user = self.request.user
        form = PostForm()
        form.author = user
        context = {
            'form': form
        }
        return render(self.request, "forum/post_form.html", context)

    def post(self, *args, **kwargs):
        user = self.request.user
        form = PostForm(self.request.POST or None)
        if form.is_valid():
            author = user
            title = form.cleaned_data.get('title')
            text = form.cleaned_data.get('text')
            post = Post(author=author, title=title, text=text)
            post.save()
            messages.success(self.request, "Your post has been added to your drafts but it has not been published yet")
            return redirect('post_draft_list', username=user.username)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update a single post and redirect to the details for
    that post. The user needs to be logged in to update a post.
    """
    def get(self, *args, **kwargs):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        form = PostEditForm(post)
        context = {
            'form': form
        }
        return render(self.request, "forum/post_edit_form.html", context)

    def post(self, *args, **kwargs):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        form = PostEditForm(post, self.request.POST or None)
        if form.is_valid():
            author = user
            title = form.cleaned_data.get('title')
            text = form.cleaned_data.get('text')
            post.author = author
            post.title = title
            post.text = text
            post.save()
            messages.success(self.request, "You have successfully edited the post")
            return redirect('post_detail', pk=post.pk)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a post and redirect to all posts"""
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(ListView):
    """Draft view for a post"""
    login_url = 'accounts/login/'
    redirect_field_name = 'post_list.html'
    model = Post
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(Q(author=user) & Q(published_date__isnull=True)).order_by('created_date')


#######################################
#######################################


def post_detail(request, pk):
    """
    Details of a single post. The is_liked boolean filter
    is passed into the template.
    """
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post,
        'total_likes': post.total_likes(),
    }
    return render(request, 'forum/post_detail.html', context)


def like_post(request, pk):
    """
    Like a specific post if the user id from the request
    does not exist in the post likes. Return count of
    total likes as a JsonResponse.
    """
    post = get_object_or_404(Post, pk=pk)
    if not post.likes.filter(id=request.user.id).exists():
        post.likes.add(request.user)
        post.likes_total += 1
        post.save()
    context = {
        'total_likes': post.likes_total,
    }
    return JsonResponse(context, safe=False)


def dislike_post(request, pk):
    """
    Like a specific post. If the like already exists
    in the database, remove the like for that user.
    """
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        post.save()
        if post.likes_total != 0:
            post.likes_total -= 1
            post.save()
    context = {
        'total_likes': post.likes_total,
    }
    return JsonResponse(context, safe=False)


@login_required
def post_publish(request, pk):
    """Allow publishing a post"""
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    messages.success(request, "Your post has been successfully published")
    return redirect('post_list')


@login_required
def add_comment_to_post(request, pk):
    """Allow adding a comment to a post"""
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = user
            comment.save()
            messages.success(request, "Your comment is pending approval...")
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'forum/comment_form.html', {'form': form})


@login_required
def add_reply_to_comment(request, pk, id):
    """Allow adding a reply to a post comment"""
    comment = get_object_or_404(Comment, id=id)
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid():
            text = request.POST.get('text')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post, reply=comment_qs,
                                             author=user, text=text,
                                             approved_comment=True)
            comment.save()
            messages.success(request, "Your reply has been successfully added")
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = CommentForm()
    return render(request, 'forum/reply_form.html',
                  {'form': form, 'comment': comment})


@login_required
def edit_reply(request, pk, id):
    """Allow editing a post comment reply"""
    comment = get_object_or_404(Comment, id=id)
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if request.method == "POST":
        form = CommentEditForm(comment, request.POST or None)
        if form.is_valid():
            text = request.POST.get('text')
            comment.text = text
            comment.author = user
            comment.save()
            messages.success(request, "You have successfully edited the reply")
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = CommentEditForm(comment)
    return render(request, 'forum/reply_edit_form.html',
                  {'form': form, 'comment': comment})


@login_required
def reply_remove(request, pk):
    """Delete a post comment reply"""
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    messages.success(request, "You have successfully removed the reply")
    return redirect('post_detail', pk=post_pk)


@login_required
def comment_approve(request, pk):
    """Approve a post comment"""
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    messages.success(request, "You have successfully approved the comment")
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    """Delete a post comment"""
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    messages.success(request, "You have successfully removed the comment")
    return redirect('post_detail', pk=post_pk)


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update a single post comment and redirect to the details for
    that post. The user needs to be logged in to update a post comment.
    """
    def get(self, *args, **kwargs):
        user = self.request.user
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        form = CommentEditForm(comment)
        form.author = user
        context = {
            'form': form
        }
        return render(self.request, "forum/comment_edit_form.html", context)

    def post(self, *args, **kwargs):
        user = self.request.user
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        form = CommentEditForm(comment, self.request.POST or None)
        if form.is_valid():
            author = user
            text = form.cleaned_data.get('text')
            comment.author = author
            comment.text = text
            comment.save()
            messages.success(self.request, "You have successfully edited the comment")
            return redirect('post_detail', pk=comment.post.pk)
