from django.shortcuts import render
from django.db.models import Q
from forum.models import Post
from django.contrib import messages
from shoppingcart.models import Item
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.http import JsonResponse
import random


def search_posts(request):
    """
    Search posts by title, text, created_date and 'published_date_isnull=False'.
    Note: searching by author does not work because author is a
    foreign key.
    """
    if request.method == "POST":
        search_text = request.POST.get('posts')
    else:
        search_text = ''

    post_list = Post.objects.filter((Q(title__icontains=search_text) |
                                     Q(text__icontains=search_text) |
                                     Q(created_date__icontains=search_text)) &
                                    Q(published_date__isnull=False))

    post_list_count = post_list.count()

    """Add pagination for searching posts"""
    paginator = Paginator(post_list, 8)
    page = request.GET.get('page')
    post_list = paginator.get_page(page)

    context = {
        'search_text': search_text,
        'post_list': post_list,
        'post_list_count': post_list_count
    }

    return render(request, 'forum/post_list.html', context)


def posts_results(request, search_text):
    if request.method == "POST":
        post_list = Post.objects.filter((Q(title__icontains=search_text) |
                                         Q(text__icontains=search_text) |
                                         Q(created_date__icontains=search_text)) &
                                        Q(published_date__isnull=False))
        if post_list.count() >= 7:
            post_list = post_list[:7]
        else:
            post_list = post_list[:post_list.count()]

        posts = []
        for post in post_list:
            dict_item = {}
            if post.title not in dict_item.keys():
                dict_item[post.title] = post.pk
            posts.append(dict_item)

        return JsonResponse(posts, safe=False)


def search_drafts(request):
    """
    Search drafts by title, text, created_date and 'published_date_isnull=True'.
    Note: searching by author does not work because author is a
    foreign key.
    """
    if request.method == "POST":
        search_text = request.POST.get('drafts')
    else:
        search_text = ''

    draft_list = Post.objects.filter((Q(title__icontains=search_text) |
                                     Q(text__icontains=search_text) |
                                     Q(created_date__icontains=search_text)) &
                                     Q(published_date__isnull=True))

    draft_list_count = draft_list.count()

    """Add pagination for searching drafts"""
    paginator = Paginator(draft_list, 8)
    page = request.GET.get('page')
    post_list = paginator.get_page(page)

    context = {
        'search_text': search_text,
        'post_list': post_list,
        'draft_list_count': draft_list_count
    }

    return render(request, 'forum/post_list.html', context)


def drafts_results(request, search_text):
    if request.method == "POST":
        draft_list = Post.objects.filter((Q(title__icontains=search_text) |
                                         Q(text__icontains=search_text) |
                                         Q(created_date__icontains=search_text)) &
                                         Q(published_date__isnull=True))
        if draft_list.count() >= 7:
            draft_list = draft_list[:7]
        else:
            draft_list = draft_list[:draft_list.count()]

        drafts = []
        for draft in draft_list:
            print(draft.author)
            dict_item = {}
            if draft.title not in dict_item.keys():
                dict_item[draft.title] = draft.pk
            if draft.author.username == request.user.username:
                drafts.append(dict_item)

        return JsonResponse(drafts, safe=False)


def search_products(request):
    """
    Search products by title, price, discount_price,
    category and description.
    """
    if request.method == "POST":
        search_text = request.POST.get('item_search')
    else:
        search_text = ''
    item_list = Item.objects.filter(Q(title__icontains=search_text) |
                                    Q(price__iexact=search_text) |
                                    Q(discount_price__iexact=search_text) |
                                    Q(category__icontains=search_text)).order_by('title')
    item_list_count = item_list.count()

    """Add pagination for search"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)

    context = {
        'search_text': search_text,
        'object_list': object_list,
        'item_list_count': item_list_count
    }

    return render(request, 'shoppingcart/home.html', context)


def products_results(request, search_text):
    if request.method == "POST":
        item_list = Item.objects.filter(Q(title__icontains=search_text) |
                                        Q(price__iexact=search_text) |
                                        Q(discount_price__iexact=search_text) |
                                        Q(category__icontains=search_text)).order_by('title')
        if item_list.count() >= 7:
            item_list = item_list[:7]
        else:
            item_list = item_list[:item_list.count()]

        items = []
        for item in item_list:
            dict_item = {}
            if item.title not in dict_item.keys():
                dict_item[item.title] = item.slug
            items.append(dict_item)

        return JsonResponse(items, safe=False)


def filter_by_dresses(request):
    """Filter products by category 'dresses'"""
    item_list = Item.objects.filter(Q(category__icontains='dresses')).order_by('title')

    """Add pagination for filter"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    context = {
        'object_list': object_list,
    }
    return render(request, 'shoppingcart/home.html', context)


def filter_by_shoes(request):
    """Filter products by category 'shoes'"""
    item_list = Item.objects.filter(Q(category__icontains='shoes')).order_by('title')

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
    item_list = Item.objects.filter(Q(category__icontains='suits')).order_by('title')

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
    item_list = Item.objects.filter(Q(category__icontains='veils')).order_by('title')

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
    item_list = Item.objects.filter(Q(category__icontains='rings')).order_by('title')

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
    item_list = Item.objects.filter(Q(category__icontains='flowers')).order_by('title')

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
    item_list = Item.objects.filter(Q(category__icontains='hair accessories')).order_by('title')

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
    item_list = Item.objects.filter(Q(category__icontains='purses')).order_by('title')

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
    item_list = Item.objects.filter(Q(category__icontains='shirts')).order_by('title')

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
    item_list = Item.objects.filter(Q(category__icontains='belts')).order_by('title')

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
    item_list = Item.objects.filter(Q(category__icontains=category)).order_by('title')

    """Add pagination for filter"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    context = {
        'object_list': object_list,
        'category': category
    }
    return render(request, 'shoppingcart/home.html', context)
