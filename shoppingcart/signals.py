# # from django.db.models.signals import post_save
# # from .models import CustomerProfile
# # from django.conf import settings


# # """Receiver for creating the customer profile"""
# # def customerprofile_receiver(sender, instance, created, *args, **kwargs):
# #     if created:
# #         customerprofile = CustomerProfile.objects.create(user=instance)
 
# # """Post save signal for creating the customer profile"""
# # post_save.connect(customerprofile_receiver, sender=settings.AUTH_USER_MODEL)
 
 
# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.core.exceptions import ObjectDoesNotExist
# from django.dispatch import receiver
# from .models import CustomerProfile

# """
# Create a profile for each new user.
# When a user is saved, the signal is sent
# which is received by the create_profile function.
# If the user was created, make a profile object
# with the instance of the user that was created.
# """
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         CustomerProfile.objects.create(user=instance)

# """
# Save the profile for each new user.
# """
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     try:
#         instance.profile.save()
#     except ObjectDoesNotExist:
#         CustomerProfile.objects.create(user=instance)