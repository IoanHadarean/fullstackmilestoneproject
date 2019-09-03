from django.test import TestCase
from django.contrib.auth.models import User


class ContactViewTest(TestCase):
    """Class for testing contact view"""

    """Set up the valid and invalid contact details + credentials for user"""
    def setUp(self):
        self.valid_details = {'name': 'Ioan123',
                              'email': 'ioan@yahoo.com',
                              'subject': 'This is a test subject',
                              'message': 'This is a test message'}
        self.invalid_details = {'name': 'Ioan123',
                                'email': '',
                                'subject': 'This is a test subject',
                                'message': 'This is a test message'}
        self.credentials = {
            'username': 'User5232lkdsa',
            'password': 'randompassword123'}
        user = User.objects.create_user(**self.credentials)
        user.save()

    """Test get contact view"""
    def test_get_contact_view(self):
        response = self.client.get('/contact/')
        self.assertTemplateUsed(response, 'contact/contact_us.html')
        self.assertEquals(response.status_code, 200)

    """
    Test for successfully sending the valid contact details
    (user is authenticated)
    """
    def test_contact_form_post_success_authenticated_user(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/contact/', self.valid_details)
        self.assertRedirects(response, '/')
        
    """
    Test for successfully sending the valid contact details
    (user is not authenticated)
    """
    def test_contact_form_post_success_not_authenticated_user(self):
        response = self.client.post('/contact/', self.valid_details)
        self.assertRedirects(response, '/')

    """Test for failing to send the invalid contact details"""
    def test_contact_form_post_fail(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/contact/', self.invalid_details)
        self.assertRedirects(response, '/contact/')
