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
    paginate_by = 5

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
    search_text = request.GET.get('item_search', '')
    item_list = Item.objects.filter(Q(title__icontains=search_text) |
                                    Q(price__iexact=search_text) |
                                    Q(discount_price__iexact=search_text) |
                                    Q(category__icontains=search_text))

    """Add pagination for search"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)

    return render(request, 'shoppingcart/home.html', {'object_list': object_list})


def filter_by_dresses(request):
    """Filter products by category 'dresses'"""
    item_list = Item.objects.filter(Q(category__icontains='dresses'))

    """Add pagination for filter"""
    paginator = Paginator(item_list, 8)
    print(paginator.num_pages)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    context = {
        'object_list': object_list,
    }
    return render(request, 'shoppingcart/home.html', context)


def filter_by_shoes(request):
    """Filter products by category 'shoes'"""
    item_list = Item.objects.filter(Q(category__icontains='shoes'))

    """Add pagination for filter"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    context = {
        'object_list': object_list,
    }
    return render(request, 'shoppingcart/home.html', context)


def filter_by_suits(request):
    """Filter products by category 'suits'"""
    item_list = Item.objects.filter(Q(category__icontains='suits'))

    """Add pagination for filter"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    context = {
        'object_list': object_list,
    }
    return render(request, 'shoppingcart/home.html', context)


def filter_by_veils(request):
    """Filter products by category 'veils'"""
    item_list = Item.objects.filter(Q(category__icontains='veils'))

    """Add pagination for filter"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    context = {
        'object_list': object_list,
    }
    return render(request, 'shoppingcart/home.html', context)


def filter_by_rings(request):
    """Filter products by category 'rings'"""
    item_list = Item.objects.filter(Q(category__icontains='rings'))

    """Add pagination for filter"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    context = {
        'object_list': object_list,
    }
    return render(request, 'shoppingcart/home.html', context)


def filter_by_flowers(request):
    """Filter products by category 'flowers'"""
    item_list = Item.objects.filter(Q(category__icontains='flowers'))

    """Add pagination for filter"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    context = {
        'object_list': object_list,
    }
    return render(request, 'shoppingcart/home.html', context)


def filter_by_hair_accessories(request):
    """Filter products by category 'hair_accessories'"""
    item_list = Item.objects.filter(Q(category__icontains='hair accessories'))

    """Add pagination for filter"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    context = {
        'object_list': object_list,
    }
    return render(request, 'shoppingcart/home.html', context)


def filter_by_purses(request):
    """Filter products by category 'purses'"""
    item_list = Item.objects.filter(Q(category__icontains='purses'))

    """Add pagination for filter"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    context = {
        'object_list': object_list,
    }
    return render(request, 'shoppingcart/home.html', context)


def filter_by_neckties(request):
    """Filter products by category 'neckties'"""
    item_list = Item.objects.filter(Q(category__icontains='neckties'))

    """Add pagination for filter"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    context = {
        'object_list': object_list,
    }
    return render(request, 'shoppingcart/home.html', context)


def filter_by_shirts(request):
    """Filter products by category 'shirts'"""
    item_list = Item.objects.filter(Q(category__icontains='shirts'))

    """Add pagination for filter"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    context = {
        'object_list': object_list,
    }
    return render(request, 'shoppingcart/home.html', context)


def filter_by_belts(request):
    """Filter products by category 'belts'"""
    item_list = Item.objects.filter(Q(category__icontains='belts'))

    """Add pagination for filter"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    context = {
        'object_list': object_list,
    }
    return render(request, 'shoppingcart/home.html', context)


def filter_by_tags(request, category):
    """Filter dinamically by product category tags"""
    item_list = Item.objects.filter(Q(category__icontains=category))

    """Add pagination for filter"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    context = {
        'object_list': object_list,
        'category': category
    }
    return render(request, 'shoppingcart/home.html', context)
