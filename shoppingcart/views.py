from django.shortcuts import render
from .models import Item

def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "shoppingcart/products.html", context)
    
    
def checkout(request):
    return render(request, "shoppingcart/checkout.html")
    

def home(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "shoppingcart/home.html", context)

