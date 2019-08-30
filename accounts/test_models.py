from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.

class TestProfileModel(TestCase):
    
    def test_str_is_equal_to_username(self):
        user = User.objects.create_user('goagl', 'hello@yahoo.com', 'randompassword')
        user.save()
        profile = Profile.objects.get(pk=1)
        self.assertEqual(str(profile), 'goagl Profile')
        
    def test_save_image(self):
        user = User.objects.create_user('goagl', 'hello@yahoo.com', 'randompassword')
        user.save()
        profile = Profile.objects.get(pk=1)
        profile.image = SimpleUploadedFile(name='BE266_rose_top.jpg', 
                                           content=open('/home/ubuntu/environment/ecommerce/media/random.jpg', 'rb').read(),
                                           content_type='image/jpeg')
        self.assertEquals(profile.save().size, (300, 169))