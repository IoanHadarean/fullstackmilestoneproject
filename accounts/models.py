from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    """
    A model class defined for a profile,
    with a default image and a one to one relationship
    with the user. The save method is overwritten
    so that the profile image is resized.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default=None, upload_to='profile_pics')
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image and hasattr(self.image, 'url'):
            img = Image.open(self.image)
            print(img)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.name)
