from django.shortcuts import render
from django.db.models import Q
from forum.models import Post
from shoppingcart.models import Item


def search_posts(request):
    """
    Search posts by title, text, created_date and 'published_date_isnull=False'.
    Note: searching by author does not work because author is a
    foreign key.
    """
    post_list = Post.objects.filter((Q(title__icontains=request.GET['posts']) | 
                    Q(text__icontains=request.GET['posts']) |
                    Q(created_date__icontains=request.GET['posts'])) & 
                    Q(published_date__isnull=False))
    return render(request, 'forum/post_list.html', {'post_list': post_list})
    
    
def search_drafts(request):
    """
    Search drafts by title, text, created_date and 'published_date_isnull=True'.
    Note: searching by author does not work because author is a
    foreign key.
    """
    post_list = Post.objects.filter((Q(title__icontains=request.GET['posts']) | 
                    Q(text__icontains=request.GET['posts']) |
                    Q(created_date__icontains=request.GET['posts'])) & 
                    Q(published_date__isnull=True))
    return render(request, 'forum/post_list.html', {'post_list': post_list})


def search_products(request):
    """
    Search products by title, price, discount_price, 
    category and description.
    """
    object_list = Item.objects.filter(Q(title__icontains=request.GET['items']) |
                        Q(price__iexact=request.GET['items']) |
                        Q(discount_price__iexact=request.GET['items']) |
                        Q(category__icontains=request.GET['items']) |
                        Q(description__icontains=request.GET['items']))
    
    return render(request, 'shoppingcart/home.html', {'object_list': object_list})
    
    
    
    
    
    
    
    
    