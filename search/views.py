from django.shortcuts import render
from django.db.models import Q
from forum.models import Post
from django.contrib import messages
from shoppingcart.models import Item
from django.core.paginator import Paginator
from django.views.generic import ListView


class SearchPosts(ListView):
    """
    Search posts by title, text, created_date and 'published_date_isnull=False'.
    Note: searching by author does not work because author is a
    foreign key.
    """
    model = Post
    paginate_by = 5
    
    def get_queryset(self):
        return Post.objects.filter((Q(title__icontains=self.request.GET['posts']) | 
                    Q(text__icontains=self.request.GET['posts']) |
                    Q(created_date__icontains=self.request.GET['posts'])) & 
                    Q(published_date__isnull=False))
    
    
class SearchDrafts(ListView):
    """
    Search drafts by title, text, created_date and 'published_date_isnull=True'.
    Note: searching by author does not work because author is a
    foreign key.
    """
    model = Post
    paginate_by = 1
    
    def get_queryset(self):
        return Post.objects.filter((Q(title__icontains=self.request.GET['posts']) | 
                    Q(text__icontains=self.request.GET['posts']) |
                    Q(created_date__icontains=self.request.GET['posts'])) & 
                    Q(published_date__isnull=True))


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


def filter_by_dresses(request, category=None):
    """Filter products by category 'dresses'"""
    object_list = Item.objects.filter(Q(category__icontains='dresses'))
    context = {
        'object_list': object_list,
        'category': category,
    }
    return render(request, 'shoppingcart/home.html', context)

def filter_by_shoes(request, category=None):
    """Filter products by category 'shoes'"""
    object_list = Item.objects.filter(Q(category__icontains='shoes'))
    context = {
        'object_list': object_list,
        'category': category,
    }
    return render(request, 'shoppingcart/home.html', context)
    
def filter_by_suits(request, category=None):
    """Filter products by category 'suits'"""
    object_list = Item.objects.filter(Q(category__icontains='suits'))
    context = {
        'object_list': object_list,
        'category': category,
    }
    return render(request, 'shoppingcart/home.html', context)

def filter_by_veils(request, category=None):
    """Filter products by category 'veils'"""
    object_list = Item.objects.filter(Q(category__icontains='veils'))
    context = {
        'object_list': object_list,
        'category': category,
    }
    return render(request, 'shoppingcart/home.html', context)
    
def filter_by_rings(request, category=None):
    """Filter products by category 'rings'"""
    object_list = Item.objects.filter(Q(category__icontains='rings'))
    context = {
        'object_list': object_list,
        'category': category,
    }
    return render(request, 'shoppingcart/home.html', context)
    
def filter_by_flowers(request, category=None):
    """Filter products by category 'flowers'"""
    object_list = Item.objects.filter(Q(category__icontains='flowers'))
    context = {
        'object_list': object_list,
        'category': category,
    }
    return render(request, 'shoppingcart/home.html', context)
    
def filter_by_hair_accessories(request, category=None):
    """Filter products by category 'hair_accessories'"""
    object_list = Item.objects.filter(Q(category__icontains='hair accessories'))
    context = {
        'object_list': object_list,
        'category': category,
    }
    return render(request, 'shoppingcart/home.html', context)
    
def filter_by_purses(request, category=None):
    """Filter products by category 'purses'"""
    object_list = Item.objects.filter(Q(category__icontains='purses'))
    context = {
        'object_list': object_list,
        'category': category,
    }
    return render(request, 'shoppingcart/home.html', context)
    
def filter_by_neckties(request, category=None):
    """Filter products by category 'neckties'"""
    object_list = Item.objects.filter(Q(category__icontains='neckties'))
    context = {
        'object_list': object_list,
        'category': category,
    }
    return render(request, 'shoppingcart/home.html', context)
    
def filter_by_shirts(request, category=None):
    """Filter products by category 'shirts'"""
    object_list = Item.objects.filter(Q(category__icontains='shirts'))
    context = {
        'object_list': object_list,
        'category': category,
    }
    return render(request, 'shoppingcart/home.html', context)
    
def filter_by_belts(request, category=None):
    """Filter products by category 'belts'"""
    object_list = Item.objects.filter(Q(category__icontains='belts'))
    context = {
        'object_list': object_list,
        'category': category,
    }
    return render(request, 'shoppingcart/home.html', context)
    
    
    
    
    
    
    