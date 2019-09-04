from django.test import TestCase
from .models import Post
from .views import PostListView
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.messages import get_messages
import datetime
import pytz


class TestForumViews(TestCase):
    
    def setUp(self):
        self.credentials = {
            'username': 'username1',
            'password': 'random'}
        self.user = User.objects.create_user(**self.credentials)
        self.user.save()
        self.post = Post(author=self.user, title='post', 
                         text='this is a post', published_date=datetime.datetime(2019, 9, 4, tzinfo=pytz.UTC))
        self.post.save()
    
    def test_get_post_list(self):
        response = self.client.get('/forum/')
        post_list_qs = list(response.context['post_list'])
        filtered_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        self.assertQuerysetEqual(filtered_posts, [repr(post) for post in post_list_qs])
    
    def test_get_user_post_list(self):
        response = self.client.get('/forum/user/username1/')
        user_post_list_qs = list(response.context['post_list'])
        user_filtered_posts = Post.objects.filter(author=self.user, published_date__isnull=False).order_by('-published_date')
        self.assertQuerysetEqual(user_filtered_posts, [repr(post) for post in user_post_list_qs])
    
    def test_get_create_post_view(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get('/forum/posts/new/')
        self.assertTemplateUsed(response, 'forum/post_form.html')
        
    def test_post_create_announce_view(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/forum/posts/new/', {'title': 'post', 'text': 'post'})
        self.assertRedirects(response, '/forum/drafts/username1/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your post has been added to your drafts but it has not been published yet')
        
    def test_get_post_update_view(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get('/forum/post/1/edit/')
        self.assertTemplateUsed(response, 'forum/post_edit_form.html')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        