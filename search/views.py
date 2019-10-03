from django.shortcuts import render
from django.db.models import Q
from forum.models import Post
from django.contrib import messages
from shoppingcart.models import Item
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import operator
from functools import reduce


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

    if len(search_text) == 1:
        cleaned_search_text = search_text.strip().split()
        query_set = reduce(operator.__or__, [(Q(title__istartswith=word) |
                                              Q(created_date__icontains=word)) &
                                             Q(published_date__isnull=False) for word in cleaned_search_text],
                           Q(title__istartswith=cleaned_search_text))
    else:
        cleaned_search_text = search_text.strip().split()
        query_set = reduce(operator.__or__, ([(Q(title__istartswith=word) |
                                               Q(title__icontains=word) |
                                               Q(created_date__icontains=word)) &
                                              Q(published_date__isnull=False) for word in cleaned_search_text if len(word) > 1] and
                                             [Q(title__istartswith=word) &
                                              Q(published_date__isnull=False) for word in cleaned_search_text if len(word) == 1]) or
                                            ([(Q(title__istartswith=word) |
                                               Q(title__icontains=word) |
                                               Q(created_date__icontains=word)) &
                                              Q(published_date__isnull=False) for word in cleaned_search_text if len(word) > 1] or
                                             [Q(title__istartswith=word) &
                                              Q(published_date__isnull=False) for word in cleaned_search_text if len(word) == 1]),
                           Q(title__istartswith=cleaned_search_text))

    post_list = Post.objects.filter(query_set).order_by('title')

    post_list_count = post_list.count()

    """Add pagination for searching posts"""
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    post_list = paginator.get_page(page)

    context = {
        'search_text': search_text,
        'post_list': post_list,
        'post_list_count': post_list_count
    }

    return render(request, 'forum/post_list.html', context)


def posts_results(request, search_text):

    """
    Get the first seven post results (post titles) according
    to the search text and return them as JSON
    """
    if request.method == "POST":

        if len(search_text) == 1:
            cleaned_search_text = search_text.strip().split()
            query_set = reduce(operator.__or__, [(Q(title__istartswith=word) |
                                                  Q(created_date__icontains=word)) &
                                                 Q(published_date__isnull=False) for word in cleaned_search_text],
                               Q(title__istartswith=cleaned_search_text))
        else:
            cleaned_search_text = search_text.strip().split()
            query_set = reduce(operator.__or__, ([(Q(title__istartswith=word) |
                                                   Q(title__icontains=word) |
                                                   Q(created_date__icontains=word)) &
                                                  Q(published_date__isnull=False) for word in cleaned_search_text if len(word) > 1] and
                                                 [Q(title__istartswith=word) &
                                                  Q(published_date__isnull=False) for word in cleaned_search_text if len(word) == 1]) or
                                                ([(Q(title__istartswith=word) |
                                                   Q(title__icontains=word) |
                                                   Q(created_date__icontains=word)) &
                                                  Q(published_date__isnull=False) for word in cleaned_search_text if len(word) > 1] or
                                                 [Q(title__istartswith=word) &
                                                  Q(published_date__isnull=False) for word in cleaned_search_text if len(word) == 1]),
                               Q(title__istartswith=cleaned_search_text))

        post_list = Post.objects.filter(query_set).order_by('title')

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


@login_required
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

    if len(search_text) == 1:
            cleaned_search_text = search_text.strip().split()
            query_set = reduce(operator.__or__, [(Q(title__istartswith=word) |
                                                  Q(created_date__icontains=word)) &
                                                 Q(published_date__isnull=True) for word in cleaned_search_text],
                               Q(title__istartswith=cleaned_search_text))
    else:
        cleaned_search_text = search_text.strip().split()
        query_set = reduce(operator.__or__, ([(Q(title__istartswith=word) |
                                               Q(title__icontains=word) |
                                               Q(created_date__icontains=word)) &
                                              Q(published_date__isnull=True) for word in cleaned_search_text if len(word) > 1] and
                                             [Q(title__istartswith=word) &
                                              Q(published_date__isnull=True) for word in cleaned_search_text if len(word) == 1]) or
                                            ([(Q(title__istartswith=word) |
                                               Q(title__icontains=word) |
                                               Q(created_date__icontains=word)) &
                                              Q(published_date__isnull=True) for word in cleaned_search_text if len(word) > 1] or
                                             [Q(title__istartswith=word) &
                                              Q(published_date__isnull=True) for word in cleaned_search_text if len(word) == 1]),
                           Q(title__istartswith=cleaned_search_text))

    draft_list = Post.objects.filter(query_set).order_by('title')

    draft_list_count = draft_list.count()

    """Add pagination for searching drafts"""
    paginator = Paginator(draft_list, 6)
    page = request.GET.get('page')
    post_list = paginator.get_page(page)

    context = {
        'search_text': search_text,
        'post_list': post_list,
        'draft_list_count': draft_list_count
    }

    return render(request, 'forum/post_list.html', context)


@login_required
def drafts_results(request, search_text):

    """
    Get the first seven draft results (draft titles) according
    to the search text and return them as JSON
    """

    if request.method == "POST":

        if len(search_text) == 1:
            cleaned_search_text = search_text.strip().split()
            query_set = reduce(operator.__or__, [(Q(title__istartswith=word) |
                                                  Q(created_date__icontains=word)) &
                                                 Q(published_date__isnull=True) for word in cleaned_search_text],
                               Q(title__istartswith=cleaned_search_text))
        else:
            cleaned_search_text = search_text.strip().split()
            query_set = reduce(operator.__or__, ([(Q(title__istartswith=word) |
                                                   Q(title__icontains=word) |
                                                   Q(created_date__icontains=word)) &
                                                  Q(published_date__isnull=True) for word in cleaned_search_text if len(word) > 1] and
                                                 [Q(title__istartswith=word) &
                                                  Q(published_date__isnull=True) for word in cleaned_search_text if len(word) == 1]) or
                                                ([(Q(title__istartswith=word) |
                                                   Q(title__icontains=word) |
                                                   Q(created_date__icontains=word)) &
                                                  Q(published_date__isnull=True) for word in cleaned_search_text if len(word) > 1] or
                                                 [Q(title__istartswith=word) &
                                                  Q(published_date__isnull=True) for word in cleaned_search_text if len(word) == 1]),
                               Q(title__istartswith=cleaned_search_text))

        draft_list = Post.objects.filter(query_set).order_by('title')

        if draft_list.count() >= 7:
            draft_list = draft_list[:7]
        else:
            draft_list = draft_list[:draft_list.count()]

        drafts = []
        for draft in draft_list:
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

    if len(search_text) == 1:
        cleaned_search_text = search_text.strip().split()
        query_set = reduce(operator.__or__, [Q(title__istartswith=word) |
                                             Q(price__iexact=word) |
                                             Q(discount_price__iexact=word) for word in cleaned_search_text],
                           Q(title__istartswith=cleaned_search_text))
    else:
        cleaned_search_text = search_text.strip().split()
        query_set = reduce(operator.__or__, ([Q(title__istartswith=word) |
                                              Q(title__icontains=word) |
                                              Q(category__icontains=word) |
                                              Q(price__iexact=word) |
                                              Q(discount_price__iexact=word) for word in cleaned_search_text if len(word) > 1] and
                                             [Q(title__istartswith=word) for word in cleaned_search_text if len(word) == 1]) or
                                            ([Q(title__istartswith=word) |
                                              Q(title__icontains=word) |
                                              Q(category__icontains=word) |
                                              Q(price__iexact=word) |
                                              Q(discount_price__iexact=word) for word in cleaned_search_text if len(word) > 1] or
                                             [Q(title__istartswith=word) for word in cleaned_search_text if len(word) == 1]),
                           Q(title__istartswith=cleaned_search_text))

    item_list = Item.objects.filter(query_set).order_by('title')

    all_items = Item.objects.all()

    item_list_count = item_list.count()

    """Add pagination for search"""
    paginator = Paginator(item_list, 8)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)

    context = {
        'search_text': search_text,
        'object_list': object_list,
        'all_items': all_items,
        'item_list_count': item_list_count
    }

    return render(request, 'shoppingcart/home.html', context)


def products_results(request, search_text):

    """
    Get the first seven product results (product titles) according
    to the search text and return them as JSON
    """
    if request.method == "POST":

        if len(search_text) == 1:
            cleaned_search_text = search_text.strip().split()
            query_set = reduce(operator.__or__, [Q(title__istartswith=word) |
                                                 Q(price__iexact=word) |
                                                 Q(discount_price__iexact=word) for word in cleaned_search_text],
                               Q(title__istartswith=cleaned_search_text))
        else:
            cleaned_search_text = search_text.strip().split()
            query_set = reduce(operator.__or__, ([Q(title__istartswith=word) |
                                                  Q(title__icontains=word) |
                                                  Q(category__icontains=word) |
                                                  Q(price__iexact=word) |
                                                  Q(discount_price__iexact=word) for word in cleaned_search_text if len(word) > 1] and
                                                 [Q(title__istartswith=word) for word in cleaned_search_text if len(word) == 1]) or
                                                ([Q(title__istartswith=word) |
                                                  Q(title__icontains=word) |
                                                  Q(category__icontains=word) |
                                                  Q(price__iexact=word) |
                                                  Q(discount_price__iexact=word) for word in cleaned_search_text if len(word) > 1] or
                                                 [Q(title__istartswith=word) for word in cleaned_search_text if len(word) == 1]),
                               Q(title__istartswith=cleaned_search_text))

        item_list = Item.objects.filter(query_set).order_by('title')

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
