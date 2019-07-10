from django import template
from shoppingcart.models import Order

# Register template tag
register = template.Library()

"""Get the cart item count for each user if
user is authenticated, else return 0"""
@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    else:
        return 0