from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Item, OrderItem, Order

    
def checkout(request):
    """
    Form for an order checkout
    """
    return render(request, "shoppingcart/checkout.html")
    

class HomeView(ListView):
    """
    View for home page with all the products
    """
    model = Item
    template_name = "shoppingcart/home.html"


class ItemDetailView(DetailView):
    """
    View for for a single product
    """
    model = Item
    template_name = "shoppingcart/product.html"
    
    
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("product", slug=slug)
    

