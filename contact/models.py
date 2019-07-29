from django.db import models


class Enquiry(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=False, null=False)
    message = models.TextField(max_length=500)
    
    class Meta:
        verbose_name_plural = 'Enquiries'
