from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, View
from django.utils import timezone
from django.db.models import Q
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm, UpdateCardForm
from accounts.models import Profile
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

"""Fetch the users card list"""


def fetchCards(profile):
    cards = stripe.Customer.list_sources(
                    profile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
    card_list = cards['data']
    return card_list

"""
Delete a card from the saved cards.
If the default card is deleted, the next one
becomes the default card.
"""


@login_required
def delete_card(request, id):
    customerprofile = Profile.objects.get(user=request.user)
    stripe.Customer.delete_source(customerprofile.stripe_customer_id, id)
    messages.success(request, "You have successfully removed the saved card")
    return redirect("payment", payment_option="stripe")

"""
Set a saved card as a default card.
The current default card becomes
a saved card.
"""


@login_required
def save_default_card(request, id):
    customerprofile = Profile.objects.get(user=request.user)
    if customerprofile.stripe_customer_id != '' and customerprofile.stripe_customer_id is not None:
        customer = stripe.Customer.retrieve(
            customerprofile.stripe_customer_id
        )
    customer.default_source = id
    customer.save()
    messages.success(request, "You have successfully set the new default card")
    return redirect("payment", payment_option="stripe")


class CheckoutView(LoginRequiredMixin, View):
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
            messages.info(self.request, "You do not have an active order")
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
                Get the form checkbox inputs and the shipping/billing address querysets.
                """
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address = form.cleaned_data.get('same_billing_address')
                address_qs_shipping = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                address_qs_billing = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                """
                If the 'same_billing_address' is not checked
                verify if the user wants to use default shipping/billing.
                If yes, then get then default shipping address and/or billing address
                from the database, else get the shipping and/or billing address from
                the inputs. If there already is a default shipping and/or billing
                address and the user wants to save a new shipping and/or billing
                address, overwrite the old one in the database, else insert a new
                shipping and/or billing address in the database.
                """
                if not same_billing_address:
                    order.same_billing_address = False
                    if use_default_shipping:
                        order.use_default_shipping = True
                        if order.save_default_shipping is True:
                            order.save_default_shipping = False
                        if address_qs_shipping.exists():
                            shipping_address = address_qs_shipping[0]
                            order.shipping_address = shipping_address
                            order.save()
                        else:
                            messages.info(self.request, "No default shipping address available")
                            return redirect('checkout')
                    else:
                        order.use_default_shipping = False
                        shipping_address1 = form.cleaned_data.get('shipping_address')
                        shipping_address2 = form.cleaned_data.get('shipping_address2')
                        shipping_country = form.cleaned_data.get('shipping_country')
                        shipping_zip_code = form.cleaned_data.get('shipping_zip_code')

                        """Check if the form fields are valid(not empty)"""
                        if is_valid_form([shipping_address1, shipping_address2, shipping_country, shipping_zip_code]):
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
                                order.save_default_shipping = True
                                if not address_qs_shipping.exists():
                                    shipping_address.default = True
                                    shipping_address.save()
                                else:
                                    address_qs_shipping.update(street_address=shipping_address1,
                                                               appartment_address=shipping_address2,
                                                               country=shipping_country,
                                                               zip_code=shipping_zip_code)
                        else:
                            messages.info(self.request, "Please fill in the required shipping address fields")
                            return redirect("checkout")

                    if use_default_billing:
                        order.use_default_billing = True
                        if order.save_default_billing is True:
                            order.save_default_billing = False
                        if address_qs_billing.exists():
                            billing_address = address_qs_billing[0]
                            order.billing_address = billing_address
                            order.save()
                        else:
                            messages.info(self.request, "No default billing address available")
                            return redirect('checkout')
                    else:
                        order.use_default_billing = False
                        billing_address1 = form.cleaned_data.get('billing_address')
                        billing_address2 = form.cleaned_data.get('billing_address2')
                        billing_country = form.cleaned_data.get('billing_country')
                        billing_zip_code = form.cleaned_data.get('billing_zip_code')

                        """Check if the form fields are valid(not empty)"""
                        if is_valid_form([billing_address1, billing_address2, billing_country, billing_zip_code]):
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
                                order.save_default_billing = True
                                if not address_qs_billing.exists():
                                    billing_address.default = True
                                    billing_address.save()
                                else:
                                    address_qs_billing.update(street_address=billing_address1,
                                                              appartment_address=billing_address2,
                                                              country=billing_country,
                                                              zip_code=billing_zip_code)
                        else:
                            messages.info(self.request, "Please fill in the required billing address fields")
                            return redirect("checkout")
                """
                If the user wants to have the same billing address as the shipping
                address, get the shipping address inputs from the form, add it to the
                order, then add the billing to the order, which is the same as the shipping
                address. Verify if the user wants to set a default shipping address.
                If there already is a default shipping address and the user wants to save a new
                shipping address, overwrite the old one in the database, else insert the new
                default address into the database.
                """
                if same_billing_address:
                    order.same_billing_address = True
                    if order.save_default_billing is True:
                        order.save_default_billing = False
                    if order.use_default_billing is True:
                        order.use_default_billing = False
                    """Use default shipping address and set it as billing address too"""
                    if use_default_shipping:
                        order.use_default_shipping = True
                        if order.save_default_shipping is True:
                            order.save_default_shipping = False
                        if address_qs_shipping.exists():
                            shipping_address = address_qs_shipping[0]
                            billing_address = address_qs_shipping[0]
                            order.shipping_address = shipping_address
                            order.billing_address = billing_address
                            order.save()
                        else:
                            messages.info(self.request, "No default shipping address available")
                            return redirect('checkout')
                    else:
                        order.use_default_shipping = False
                        shipping_address1 = form.cleaned_data.get('shipping_address')
                        shipping_address2 = form.cleaned_data.get('shipping_address2')
                        shipping_country = form.cleaned_data.get('shipping_country')
                        shipping_zip_code = form.cleaned_data.get('shipping_zip_code')

                        """Check if the form fields are valid(not empty)"""
                        if is_valid_form([shipping_address1, shipping_address2, shipping_country, shipping_zip_code]):
                            shipping_address = Address(
                                user=self.request.user,
                                street_address=shipping_address1,
                                appartment_address=shipping_address2,
                                country=shipping_country,
                                zip_code=shipping_zip_code,
                                address_type='S'
                            )
                            shipping_address.save()

                            billing_address = Address(
                                user=self.request.user,
                                street_address=shipping_address1,
                                appartment_address=shipping_address2,
                                country=shipping_country,
                                zip_code=shipping_zip_code,
                                address_type='B'
                            )
                            billing_address.save()

                            order.shipping_address = shipping_address
                            order.billing_address = billing_address
                            order.save()

                            """Set the default shipping/billing address"""
                            set_default_shipping = form.cleaned_data.get('set_default_shipping')
                            if set_default_shipping:
                                order.save_default_shipping = True
                                if not address_qs_shipping.exists():
                                    shipping_address.default = True
                                    shipping_address.save()
                                else:
                                    address_qs_shipping.update(street_address=shipping_address1,
                                                               appartment_address=shipping_address2,
                                                               country=shipping_country,
                                                               zip_code=shipping_zip_code)
                                if not address_qs_billing.exists():
                                    billing_address.default = True
                                    billing_address.save()
                                else:
                                    address_qs_billing.update(street_address=shipping_address1,
                                                              appartment_address=shipping_address2,
                                                              country=shipping_country,
                                                              zip_code=shipping_zip_code)
                        else:
                            messages.info(self.request, "Please fill in the required shipping address fields")
                            return redirect("checkout")
                payment_option = form.cleaned_data.get('payment_option')
                order.payment_option = payment_option
                order.save()

                """Redirect according to payment option"""
                if payment_option == 'S':
                    return redirect('payment', payment_option='stripe')
            else:
                messages.warning(self.request, "Invalid data")
                return redirect("checkout")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order_summary")


class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        """Render the payment view and pass the order to the template"""
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            customerprofile = Profile.objects.get(user=self.request.user)
            if customerprofile.stripe_customer_id != '' and customerprofile.stripe_customer_id is not None:
                customer = stripe.Customer.retrieve(
                    customerprofile.stripe_customer_id
                )
            if customerprofile.one_click_purchasing:
                card_list = fetchCards(customerprofile)
                for card in card_list:
                    if customer.default_source == card.id:
                        context.update({
                            'default_card': card
                        })
                if len(card_list) > 0:
                    """Update the context with the default credit cards"""
                    context.update({
                        'saved_cards': card_list
                    })
            return render(self.request, "shoppingcart/payment.html", context)
        else:
            messages.warning(self.request, "You did not add a billing address")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        """ Get the stripe token and create a charge for a user order"""
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        customerprofile = Profile.objects.get(user=self.request.user)
        if customerprofile.one_click_purchasing:
            card_list = fetchCards(customerprofile)

        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            """Allow fetching cards from stripe"""
            if save:
                """
                If there is not a customer id associated on the
                customer profile, create the stripe customer and save it,
                else create a source for the customer if there are no more
                than three saved cards
                """
                if customerprofile.stripe_customer_id != '' and customerprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        customerprofile.stripe_customer_id
                    )
                    if len(card_list) < 3:
                        customer.sources.create(source=token)
                    else:
                        messages.warning(self.request, "We are sorry, but you can not save more than 3 cards. Please consider removing one of the saved cards!")
                        return redirect("payment", payment_option="stripe")
                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email
                    )
                    customer.sources.create(source=token)
                    customerprofile.stripe_customer_id = customer['id']
                    customerprofile.one_click_purchasing = True
                    customerprofile.save()

            amount = int(order.get_total() * 100)

            try:
                """If the customer uses a default card pass the
                customer to the charge, else pass the source"""
                if use_default or save:
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

                messages.success(self.request, "Your order was successful! We have sent you a confirmation email")
                send_mail(
                    'Wedding Planner order',
                    """
                    Your order was successful!
                    Thank you for shopping with us!
                    Your order reference code is: {}""".format(order.ref_code),
                    'weddingplanner@email.com',
                    [self.request.user.email],
                    fail_silently=False,
                    )
                return redirect("/")
            except stripe.error.CardError as e:
                """Since it's a decline, stripe.error.CardError will be caught"""
                body = e.json_body
                err = body.get('error', {})
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
                send_mail(
                    'Stripe error',
                    """
                    A stripe error has occured.
                    Please take action!
                    """,
                    'weddingplanner@email.com',
                    ['admin@example.com'],
                    fail_silently=False,
                    )
                messages.warning(self.request, "Something went wrong.You were not charged.Please try again.")
                return redirect("/")
            except Exception as e:
                """Send an email to the user"""
                messages.warning(self.request, "A serious error occured. We have been notified.")
                send_mail(
                    'Wedding Planner order',
                    """
                    Your order was unsuccessful!
                    We are sorry that you had to go through this!
                    If you were charged, please do not hesitate
                    to ask for a refund or to contact us!
                    Your order reference code is: {}""".format(order.ref_code),
                    'weddingplanner@email.com',
                    [self.request.user.email],
                    fail_silently=False,
                    )
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


def item_detail(request, slug):
    """
    View for a single product
    """
    item = get_object_or_404(Item, slug=slug)
    """Get random 4 items with the same category as the detail view item"""
    category_items = Item.objects.filter(category=item.category).exclude(title=item.title).values_list('id', flat=True).order_by('title')
    random_items_id_list = random.sample(list(category_items), min(len(category_items), 4))
    random_category_items = Item.objects.filter(id__in=random_items_id_list).order_by('title')
    context = {
        'item': item,
        'random_category_items': random_category_items
    }
    return render(request, 'shoppingcart/product.html', context)


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
                messages.info(request, "This item quantity was updated.")
                return redirect("order_summary")
            else:
                order.items.remove(order_item)
                messages.info(request, "This item was removed from your cart.")
                return redirect("order_summary")
        else:
            messages.info(request, "This item is not in your cart.")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("product", slug=slug)


class AddCouponView(LoginRequiredMixin, View):
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
                    """
                    Get or create a user coupon with the user from the request
                    if the order does not have a coupon yet. Assign the coupon to the
                    order and the user coupon specific to the user that made the order.
                    If the order already has a coupon try to get the coupon from the user
                    coupons and if it does not exist notify the user that he can not use
                    more than one coupon for an order.
                    """
                    if order.used_coupon is False:
                        user_coupon = UserCoupon.objects.get_or_create(user=self.request.user, coupon=get_coupon)
                        if user_coupon[0].is_used is False:
                            order.coupon = get_coupon
                            order.user_coupon = user_coupon[0]
                        order.save()
                    else:
                        try:
                            """Get the coupon corresponding to a certain user"""
                            user_coupon = UserCoupon.objects.get(user=self.request.user, coupon=get_coupon)
                        except ObjectDoesNotExist:
                            messages.warning(self.request, "You can not use more than one coupon for an order")
                            return redirect("checkout")
                except ObjectDoesNotExist:
                    messages.info(self.request, "This coupon does not exist or is no longer active")
                    return redirect("checkout")
                """
                Check if no other coupon has been used for that order and if there is a
                user coupon.
                Check if the coupon total is not more than the value of the order
                and if the user has not already used that coupon.
                """
                if user_coupon and order.used_coupon is False:
                    if order.get_total_with_coupon() > 0 and user_coupon[0].is_used is False:
                        user_coupon[0].is_used = True
                        order.used_coupon = True
                        if order.coupon.number_of_usages_allowed > 0:
                            order.coupon.number_of_usages_allowed -= 1
                            order.coupon.save()
                        else:
                            order.coupon.active = False
                            order.coupon.save()
                        user_coupon[0].save()
                        order.save()
                        messages.success(self.request, "Successfully added coupon")
                        return redirect("checkout")
                    elif order.get_total_with_coupon() > 0 and user_coupon[0].is_used is True:
                        messages.warning(self.request, "You have already used this coupon")
                        return redirect("checkout")
                    elif order.get_total_with_coupon() <= 0:
                        messages.warning(self.request, "You can not use this coupon for items with the price less than or equal to the value of the coupon")
                        return redirect("checkout")
                elif user_coupon and order.used_coupon is True:
                    messages.warning(self.request, "You can not use more than one coupon for an order")
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
            name = form.cleaned_data.get('name')
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
                refund.name = name
                refund.save()

                messages.info(self.request, "Your refund request was received.")
                return redirect("request_refund")
            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist. Please check your email for the correct reference code.")
                return redirect("request_refund")


class UpdateCardView(LoginRequiredMixin, View):

    """Render the update card form in the template"""
    def get(self, *args, **kwargs):
        form = UpdateCardForm()
        context = {
            'form': form
        }
        return render(self.request, "shoppingcart/update_card.html", context)

    """Post the update card form details"""
    def post(self, *args, **kwargs):
        form = UpdateCardForm(self.request.POST or None)
        customerprofile = Profile.objects.get(user=self.request.user)
        card_id = self.kwargs['id']
        is_default_source = False
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            if customerprofile.stripe_customer_id != '' and customerprofile.stripe_customer_id is not None:
                customer = stripe.Customer.retrieve(
                    customerprofile.stripe_customer_id
                )
                if customer.default_source == card_id:
                    is_default_source = True
            stripe.Customer.delete_source(customerprofile.stripe_customer_id, card_id)
            updated_source = stripe.Customer.create_source(customerprofile.stripe_customer_id, source=token)
            if is_default_source is True:
                customer.default_source = updated_source.id
                customer.save()
            messages.success(self.request, "Your card details have been updated successfully")
            return redirect("payment", payment_option="stripe")
        else:
            messages.warning(self.request, "Invalid credit card details")
            return redirect("payment", payment_option="stripe")
