from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .forms import CheckoutForm
from .models import Item, OrderItem, Order, BillingAddress


class CheckoutView(View):
    """
    Form for an order checkout
    """
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "shoppingcart/checkout.html", context)
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        """
        Check if the order exists. If it does, get the details of the order
        from the form if the form is valid and save the billing address, else
        raise an error saying that the user does not have an active order.
        """
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                appartment_address = form.cleaned_data.get('appartment_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                """TODO: add functionality for these fields
                same_shipping_address = form.cleaned_data.get(
                'same_shipping_address')
                save_info = form.cleaned_data.get('save_info')"""
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    appartment_address=appartment_address,
                    country=country,
                    zip_code=zip_code
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                """TODO: add redirect to the selected payment option"""
                return redirect('checkout')
            messages.warning(self.request, "Failed checkout")
            return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("order_summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "shoppingcart/payment.html")


class HomeView(ListView):
    """
    View for home page with all the products
    """
    model = Item
    paginate_by = 10
    template_name = "shoppingcart/home.html"
    
    
class OrderSummaryView(LoginRequiredMixin, View):
    """
    Get the order summary for a user if it exists,
    else show an error stating that the user does not
    have an active order
    """
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'shoppingcart/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    """
    View for for a single product
    """
    model = Item
    template_name = "shoppingcart/product.html"
    
@login_required    
def add_to_cart(request, slug):
    """
    Get the item that needs to be added to cart or show a 404 error.
    Then get or create the order item that corresponds to a user and
    has an ordered attribute of False.
    Filter the orders by the user and by the 'ordered=False' attribute.
    If the order query set exists, check if the order item is in the order.
    If it is then increase the quantity by 1 each time it's added to the cart,
    else add it to the order.
    If the order query set does not exist, create a new order that has an ordered
    date and a user and add the order item to the order.
    """
    
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        """Check if the order item is in the order"""
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order_summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order_summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order_summary")
    
@login_required 
def remove_from_cart(request, slug):
    """
    Get the item that needs to be added to cart or show a 404 error.
    Filter the orders by the user and by the 'ordered=False' attribute.
    If the order query set exists, check if the order item is in the order.
    If it is, get the order item and remove it from the orders, else
    display a message saying the item is not in the cart.
    If the order query set does not exist display a message saying the user
    does not have an order.
    """
    
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        """ Check if the order item is in the order"""
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("order_summary")
        else:
            messages.info(request, "This item is not in your cart.")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("product", slug=slug)
        
@login_required 
def remove_single_item_from_cart(request, slug):
    """
    Get the item that needs to be added to cart or show a 404 error.
    Filter the orders by the user and by the 'ordered=False' attribute.
    If the order query set exists, check if the order item is in the order.
    If it is, get the order item and decrease the quantity by 1, else
    display a message saying the item is not in the cart.
    If the order query set does not exist display a message saying the user
    does not have an active order.
    """
    
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        """ Check if the order item is in the order"""
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated")
            return redirect("order_summary")
        else:
            messages.info(request, "This item is not in your cart.")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("product", slug=slug)