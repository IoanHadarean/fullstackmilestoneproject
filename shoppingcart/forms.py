from django import forms
from django_countries.fields import CountryField


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
)


class CheckoutForm(forms.Form):
    """
    Checkout form details, including a shipping address and
    a billing address. Has the options to use a default shipping
    address and to set the billing address the same as the
    shipping address.
    """
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_zip_code = forms.CharField(required=False)
    shipping_country = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_zip_code = forms.CharField(required=False)
    billing_country = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    """Coupon form that takes a code"""
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
    }))


class RefundForm(forms.Form):
    """
    Refund form with the reference code
    and a message
    """
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
    }))
    email = forms.CharField(min_length=11, required=True,  widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'type': 'email',
    }))
    ref_code = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'ref_code',
    }))
    message = forms.CharField(max_length=500, required=True, widget=forms.Textarea(attrs={
        'rows': 2,
        'class': 'form-control md-textarea',
        'id': 'message',
    }))


class PaymentForm(forms.Form):
    """
    Payment form with the stripe token and
    save and use_default fields for credit card
    """
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
    delete_card = forms.CharField(required=False)
    
    
class UpdateCardForm(forms.Form):
    """
    Form for updating a credit/debit card
    """
    stripeToken = forms.CharField(required=False)

