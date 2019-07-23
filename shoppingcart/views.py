from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .forms import CheckoutForm, CouponForm, RefundForm
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserCoupon

import random
import stripe
import string
stripe.api_key = settings.STRIPE_SECRET_KEY

"""Create a 20 characters reference code for the order"""
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

"""Check if the form fields are empty"""
def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid
        

class CheckoutView(View):
    """
    Render the checkout form with the order if the order exists.
    If the order does not exist, notify the user that he/she does not
    have an active order.
    """
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            
            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update({'default_shipping_address': shipping_address_qs[0]})
                
            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update({'default_billing_address': billing_address_qs[0]})
            return render(self.request, "shoppingcart/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(request, "You do not have an active order")
            return redirect("checkout")
    
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
                
                """
                Check if there is a default shipping address. If it is, use the default one,
                else use the shipping address from the form fields.
                """
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address = form.cleaned_data.get('same_billing_address')
                if use_default_shipping:
                    print("Using the default shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(self.request, "No default shipping address available")
                        return redirect('checkout')
                elif not same_billing_address:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shipping_zip_code = form.cleaned_data.get('shipping_zip_code')
                    
                    """Check if the form fields are valid(not empty)"""
                    if is_valid_form([shipping_address1, shipping_country, shipping_zip_code]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            appartment_address=shipping_address2,
                            country=shipping_country,
                            zip_code=shipping_zip_code,
                            address_type='S'
                        )
                        shipping_address.save()
                        
                        order.shipping_address = shipping_address
                        order.save()
                
                        """Set the default shipping address"""
                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(self.request, "Please fill in the required shipping address fields")
                """
                First case: check if the billing address is the same as the shipping address.
                Second case: check if there is a default billing address. If it is, use the default one,
                else use the billing address from the form fields.
                """
                
                if same_billing_address:
                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shipping_zip_code = form.cleaned_data.get('shipping_zip_code')
                    if is_valid_form([shipping_address1, shipping_country, shipping_zip_code]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            appartment_address=shipping_address2,
                            country=shipping_country,
                            zip_code=shipping_zip_code,
                            address_type='S'
                        )
                        shipping_address.save()
                        
                        order.shipping_address = shipping_address
                        order.save()
                        
                        """Set the default shipping address"""
                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                            
                        billing_address = shipping_address
                        billing_address.pk = None
                        billing_address.save()
                        billing_address.address_type = 'B'
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(self.request, "Please fill in the required shipping address fields")
                        return redirect('checkout')
                
                elif use_default_billing:
                    print("Using the default billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(self.request, "No default billing address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new shipping address")
                    billing_address1 = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_zip_code = form.cleaned_data.get('billing_zip_code')
                    
                    """Check if the form fields are valid(not empty)"""
                    if is_valid_form([billing_address1, billing_country, billing_zip_code]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            appartment_address=billing_address2,
                            country=billing_country,
                            zip_code=billing_zip_code,
                            address_type='B'
                        )
                        billing_address.save()
                        
                        order.billing_address = billing_address
                        order.save()
                
                        """Set the default billing address"""
                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()
                    else:
                        messages.info(self.request, "Please fill in the required billing address fields")
                        return redirect('checkout')
                
                payment_option = form.cleaned_data.get('payment_option')
                    
                """Redirect according to payment option"""
                if payment_option == 'S':
                    return redirect('payment', payment_option='stripe')
                else:
                    messages.warning(self.request, "Invalid payment option selected")
                    return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order_summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        """Render the payment view and pass the order to the template"""
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            customerprofile = self.request.user.customerprofile
            if customerprofile.one_click_purchasing:
                """Fetch the users card list"""
                cards = stripe.Customer.list_source(
                    customerprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    """Update the context with the default credit card"""
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "shoppingcart/payment.html", context)
        else:
            messages.warning(self.request, "You did not add a billing address")
            return redirect("checkout")
            
    def post(self, *args, **kwargs):
        """ Get the stripe token and create a charge for a user order"""
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        save = form.cleaned_data.get('save')
        use_default = form.cleaned_data.get('use_default')
        
        """Allow fetching cards from stripe"""
        if save:
            """
            If there is not a customer id associated on the 
            customer profile, create the stripe customer and save it, 
            else create a source for the customer
            """
            if not customerprofile.stripe.customer_id:
                customer = stripe.Customer.create(
                    email=self.request.user.email,
                    source=token
                )
                customerprofile.customer_id = customer['id']
                customerprofile.one_click_purchasing =True
                customerprofile.save()
            else:
                stripe.Customer.create_source(
                    customerprofile.stripe.customer_id,
                    source=token
                )

        amount = int(order.get_total() * 100)
        
        try:
            """If the customer uses a default card pass the
            customer to the charge, else pass the source"""
            if use_default:
                charge = stripe.Charge.create(
                    amount=amount, 
                    currency="gbp",
                    customer=customerprofile.stripe_customer_id
                )
            else:
                charge = stripe.Charge.create(
                    amount=amount, 
                    currency="gbp",
                    source=token
                )
            
            """Create the payment"""
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()
            
            """Assign the payment to the order"""
            
            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()
                
            order.ordered = True
            order.payment = payment
            """Assign the reference code"""
            order.ref_code = create_ref_code()
            order.save()
            
            messages.success(self.request, "Your order was successful!")
            return redirect("/")
        except stripe.error.CardError as e:
            """Since it's a decline, stripe.error.CardError will be caught"""
            body = e.json_body
            err  = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("/")
        except stripe.error.RateLimitError as e:
          """Too many requests made to the API too quickly"""
          messages.warning(self.request, "Rate Limit Error")
          return redirect("/")
        except stripe.error.InvalidRequestError as e:
          """Invalid parameters were supplied to Stripe's API"""
          messages.warning(self.request, "Invalid parameters")
          return redirect("/")
        except stripe.error.AuthenticationError as e:
          """Authentication with Stripe's API failed
          (maybe you changed API keys recently)"""
          messages.warning(self.request, "Not authenticated")
          return redirect("/")
        except stripe.error.APIConnectionError as e:
          """Network communication with Stripe failed"""
          messages.warning(self.request, "Network error")
          return redirect("/")
        except stripe.error.StripeError as e:
          """Display a very generic error to the user, and maybe send
          yourself an email"""
          messages.warning(self.request, "Something went wrong.You were not charged.Please try again.")
          return redirect("/")
        except Exception as e:
          """Send an email to the user"""
          messages.warning(self.request, "A serious error occured. We have been notified.")
          return redirect("/")


class HomeView(ListView):
    """
    View for home page with all the products
    """
    model = Item
    paginate_by = 8
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
            messages.warning(self.request, "You do not have an active order")
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


class AddCouponView(View):
    """Add the cupon to the order"""
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                now = timezone.now()
                try:
                    get_coupon = Coupon.objects.get(code__iexact=code, 
                                                    valid_from__lte=now,
                                                    valid_to__gte=now,
                                                    active=True)
                    """Get or create a user coupon with the user from the request"""
                    user_coupon = UserCoupon.objects.get_or_create(user=self.request.user)
                    order.coupon = get_coupon
                    order.save()
                except ObjectDoesNotExist:
                    messages.info(self.request, "This coupon is no longer active")
                    return redirect("checkout")
                """Get the coupon corresponding to a certain user"""
                user_coupon = UserCoupon.objects.get(user=self.request.user)
                """
                Check if the coupon total is not more than the value of the order
                and if the user has not already used that coupon.
                """
                if order.get_total() > 0 and user_coupon.is_used == False:
                    user_coupon.is_used = True
                    if order.coupon.number_of_usages_allowed > 0:
                        order.coupon.number_of_usages_allowed -= 1
                        order.coupon.save()
                    else:
                        order.coupon.active = False
                        order.coupon.save()
                    user_coupon.save()
                    order.save()
                    messages.success(self.request, "Successfully added coupon")
                    return redirect("checkout")
                elif order.get_total() > 0 and user_coupon.is_used == True:
                    messages.warning(self.request, "You have already used this coupon")
                    return redirect("checkout")
                else:
                    messages.warning(self.request, "You can not use this coupon for items with the price less than the value of the coupon")
                    return redirect("checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("checkout")

        
class RequestRefundView(View):
    
    """Render the refund form in the template"""
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "shoppingcart/request_refund.html", context)
    
    """
    Post the refund form ref_code, message and email
    """
    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            """Edit the order"""
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()
                
                """Store the refund details"""
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()
                
                messages.info(self.request, "Your request was received.")
                return redirect("request_refund")
                
            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist")
                return redirect("request_refund")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        