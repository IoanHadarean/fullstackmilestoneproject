from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
from PIL import Image

CATEGORY_CHOICES = (
    ('DRESSES', 'Dresses'),
    ('SHOES', 'Shoes'),
    ('SUITS', 'Suits'),
    ('VEILS', 'Veils'),
    ('RINGS', 'Rings'),
    ('FLOWERS', 'Flowers'),
    ('HAIR ACCESSORIES', 'Hair Accessories'),
    ('PURSES', 'Purses'),
    ('SHIRTS', 'Shirts'),
    ('BELTS', 'Belts'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Item(models.Model):
    """
    Item class that contains the details of an item. Has an add_to_cart
    and a remove_from_cart method for adding/removing products from
    the cart. The save method is overwritten so that the product image
    is resized.
    """
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("add_to_cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("remove_from_cart", kwargs={'slug': self.slug})

    def get_discount_price(self):
        if self.discount_price:
            total_price = self.price - self.discount_price
        return total_price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.name)


class OrderItem(models.Model):
    """
    OrderItem class that makes the connection between
    order and item. Has a method that gets the total item
    price, a method that gets the total item discount price
    and another one that returns the amount of money saved.
    Also returns the final price depending if there is a
    discount on the item or not.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()


class Order(models.Model):
    """
    Order class that contains the details of an order.
    Has a method that gets the order summary total.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address',
        on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address',
        on_delete=models.SET_NULL, blank=True, null=True)
    use_default_shipping = models.BooleanField(default=False)
    use_default_billing = models.BooleanField(default=False)
    save_default_shipping = models.BooleanField(default=False)
    save_default_billing = models.BooleanField(default=False)
    same_billing_address = models.BooleanField(default=False)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    user_coupon = models.ForeignKey(
        'UserCoupon', on_delete=models.SET_NULL, blank=True, null=True)
    used_coupon = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    amount = models.IntegerField(blank=True, null=True)
    payment_option = models.CharField(max_length=10, default='payment')

    """
    Phases of an order:
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    """

    def __str__(self):
        return self.user.username

    """
    Get the total for all the items in the cart
    and only decrease the total if there is an user
    coupon that has not been used. The difference between
    the total of the items in the cart and the coupon amount
    should also be greater than 0.
    """

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
            self.amount = total
            self.save()
        if self.coupon and self.user_coupon and total - self.coupon.amount > 0:
            total -= self.coupon.amount
            self.amount = total
            self.save()
        return total

    """
    Get the total for all the items in the cart.
    If there is a coupon get the total
    regardless if the coupon was used or not
    or if the difference between the total of the items
    in the cart and the coupon amount is less than 0.
    This function is used for some checks in the
    'checkout.html' and 'order_summary.html' templates.
    """

    def get_total_with_coupon(self):
        total_with_coupon = 0
        for order_item in self.items.all():
            total_with_coupon += order_item.get_final_price()
        if self.coupon:
            total_with_coupon -= self.coupon.amount
        return total_with_coupon


class Address(models.Model):
    """Address details for a user"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    appartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    """Payment details for an order done by a user"""
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,
                             blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.user.username


class Coupon(models.Model):
    """Coupon code for an order item"""
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)
    number_of_usages_allowed = models.IntegerField(default=100)

    def __str__(self):
        return self.code


class UserCoupon(models.Model):
    """Coupon code for each user"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,
                             blank=True, null=True)
    is_used = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)


class Refund(models.Model):
    """Refund details for an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
