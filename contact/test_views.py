from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

class ContactViewTest(TestCase):
    
    def setUp(self):
        self.valid_details = {'name': 'Ioan123', 
                              'email': 'ioan@yahoo.com', 
                              'subject': 'This is a test subject',
                              'message': 'This is a test message',
                             }
        self.invalid_details = {'name': 'Ioan123', 
                                'email': '', 
                                'subject': 'This is a test subject',
                                'message': 'This is a test message',
                               }
        self.credentials = {
            'username': 'User5232lkdsa',
            'password': 'randompassword123'}
        user = User.objects.create_user(**self.credentials)
        user.save()

    def test_get_contact_page(self):
        # Create an instance of a GET request.
        client = Client()
        response = client.get('/contact/')
        self.assertTemplateUsed(response, 'contact/contact_us.html')
        self.assertEquals(response.status_code, 200)
        
    def test_contact_form_post_success(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/contact/', self.valid_details)
        self.assertRedirects(response, '/')
        
    def test_contact_form_post_fail(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/contact/', self.invalid_details)
        self.assertRedirects(response, '/contact/')
        
        
        