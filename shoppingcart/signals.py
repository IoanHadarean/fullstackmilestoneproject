from django.db.models.signals import post_save
from .models import CustomerProfile
from django.conf import settings


"""Receiver for creating the customer profile"""
def customerprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        customer_profile = CustomerProfile.objects.create(user=instance)
 
"""Post save signal for creating the customer profile"""
post_save.connect(customerprofile_receiver, sender=settings.AUTH_USER_MODEL)
 