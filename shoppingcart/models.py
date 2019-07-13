from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField

CATEGORY_CHOICES = (
    ('DR', 'Dresses'),
    ('SH', 'Shoes'),
    ('SU', 'Suits'),
    ('VL', 'Veils'),
    ('RN', 'Rings'),
    ('FL', 'Flowers'),
    ('HA', 'Hair Accessories'),
    ('BP', 'Bags & Purses'),
    ('NT', 'Neckties'),
    ('SH', 'Shirts'),
    ('BS', 'Belts & Sashes'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

class Item(models.Model):
    """
    Item class that contains the details of an item
    """
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse("product", kwargs={'slug': self.slug})
        
    def get_add_to_cart_url(self):
        return reverse("add_to_cart", kwargs={'slug': self.slug})
        
    def get_remove_from_cart_url(self):
        return reverse("remove_from_cart", kwargs={'slug': self.slug})

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
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    
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

    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
        
        
class BillingAddress(models.Model):
    """Billing address details for a user"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    appartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=True)
    zip_code = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username


class Payment(models.Model):
    """Payment details for an order done by a user"""
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return self.user.username
        
        
class Coupon(models.Model):
    """Coupon code for an order item"""
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    
    def __str__(self):
        return self.code