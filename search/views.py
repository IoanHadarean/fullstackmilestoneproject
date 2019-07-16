from django.shortcuts import render
from django.db.models import Q
from forum.models import Post
from django.contrib import messages
from shoppingcart.models import Item, CATEGORY_CHOICES


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
    search_text = request.GET['item_search']
    object_list = Item.objects.filter(Q(title__icontains=search_text) |
                        Q(price__iexact=search_text) |
                        Q(discount_price__iexact=search_text) |
                        Q(category__icontains=search_text) |
                        Q(description__icontains=search_text))
    return render(request, 'shoppingcart/home.html', {'object_list': object_list})


def filter_by_dresses(request):
    """Filter products by category 'dresses'"""
    object_list = Item.objects.filter(Q(category__icontains='dresses'))
    return render(request, 'shoppingcart/home.html', {'object_list': object_list})

def filter_by_shoes(request):
    """Filter products by category 'shoes'"""
    object_list = Item.objects.filter(Q(category__icontains='shoes'))
    return render(request, 'shoppingcart/home.html', {'object_list': object_list})
    
def filter_by_suits(request):
    """Filter products by category 'suits'"""
    object_list = Item.objects.filter(Q(category__icontains='suits'))
    return render(request, 'shoppingcart/home.html', {'object_list': object_list})

def filter_by_veils(request):
    """Filter products by category 'veils'"""
    object_list = Item.objects.filter(Q(category__icontains='veils'))
    return render(request, 'shoppingcart/home.html', {'object_list': object_list})
    
def filter_by_rings(request):
    """Filter products by category 'rings'"""
    object_list = Item.objects.filter(Q(category__icontains='rings'))
    return render(request, 'shoppingcart/home.html', {'object_list': object_list})
    
def filter_by_flowers(request):
    """Filter products by category 'flowers'"""
    object_list = Item.objects.filter(Q(category__icontains='flowers'))
    return render(request, 'shoppingcart/home.html', {'object_list': object_list})
    
def filter_by_hair_accessories(request):
    """Filter products by category 'hair_accessories'"""
    object_list = Item.objects.filter(Q(category__icontains='hair accessories'))
    return render(request, 'shoppingcart/home.html', {'object_list': object_list})
    
def filter_by_purses(request):
    """Filter products by category 'purses'"""
    object_list = Item.objects.filter(Q(category__icontains='purses'))
    return render(request, 'shoppingcart/home.html', {'object_list': object_list})
    
def filter_by_neckties(request):
    """Filter products by category 'neckties'"""
    object_list = Item.objects.filter(Q(category__icontains='neckties'))
    return render(request, 'shoppingcart/home.html', {'object_list': object_list})
    
def filter_by_shirts(request):
    """Filter products by category 'shirts'"""
    object_list = Item.objects.filter(Q(category__icontains='shirts'))
    return render(request, 'shoppingcart/home.html', {'object_list': object_list})
    
def filter_by_belts(request):
    """Filter products by category 'belts'"""
    object_list = Item.objects.filter(Q(category__icontains='belts'))
    return render(request, 'shoppingcart/home.html', {'object_list': object_list})
    
    
    
    
    
    
    