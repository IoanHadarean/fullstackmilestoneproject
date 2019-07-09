from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item

    
def checkout(request):
    return render(request, "shoppingcart/checkout.html")
    

class HomeView(ListView):
    model = Item
    template_name = "shoppingcart/home.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "shoppingcart/product.html"

