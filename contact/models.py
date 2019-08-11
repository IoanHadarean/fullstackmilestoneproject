from django.db import models


class Enquiry(models.Model):

    """Enquiry class for storing the contact form details"""

    name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=False, null=False)
    message = models.TextField(max_length=500)

    class Meta:
        verbose_name_plural = 'Enquiries'
