from django.shortcuts import render
from django.db.models import Q
from forum.models import Post

def search_posts(request):
    """
    Search posts by title, text, created_date and published_date.
    Note: searching by author does not work because author is a
    foreign key.
    """
    post_list = Post.objects.filter(Q(title__icontains=request.GET['posts']) | 
                    Q(text__icontains=request.GET['posts']) |
                    Q(created_date__icontains=request.GET['posts']) | 
                    Q(published_date__icontains=request.GET['posts']))
    return render(request, 'forum/post_list.html', {'post_list': post_list})
