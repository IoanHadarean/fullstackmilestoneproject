from django.test import TestCase
from .models import Post, Comment
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
        self.post = Post(author=self.user, title='post', likes_total=100,
                         text='this is a post', published_date=datetime.datetime(2019, 9, 4, tzinfo=pytz.UTC))
        self.post.save()
        self.comment = Comment(author=self.user, post=self.post, text='comment')
        self.comment.save()
    
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
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your post has been added to your drafts but it has not been published yet')
        self.assertRedirects(response, '/forum/drafts/username1/')
        
    def test_get_post_update_view(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get('/forum/post/1/edit/')
        self.assertTemplateUsed(response, 'forum/post_edit_form.html')
        
    def test_post_announce_update_view(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/forum/post/1/edit/', {'title': 'edited post', 'text': 'edited text'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have successfully edited the post')
        self.assertRedirects(response, '/forum/post/1/')
        
    def test_like_post(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/forum/post/1/like/')
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'total_likes': 101})

    def test_dislike_post(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        self.post.likes.add(self.user)
        self.post.save()
        response = self.client.post('/forum/post/1/dislike/')
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'total_likes': 99})
    
    def test_post_publish(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/forum/post/1/publish/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your post has been successfully published')
        self.assertRedirects(response, '/forum/')
        
    def test_get_add_comment_to_post_view(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get('/forum/post/1/comment/')
        self.assertTemplateUsed(response, 'forum/comment_form.html')
        
    def test_post_add_comment_to_announce(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/forum/post/1/comment/', {'text': 'comment'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your comment is pending approval...')
        self.assertRedirects(response, '/forum/post/1/')
        
    def test_get_add_reply_to_comment_view(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get('/forum/post/1/comment/1/reply/')
        self.assertTemplateUsed(response, 'forum/reply_form.html')
        
    def test_post_add_reply_to_comment(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/forum/post/1/comment/1/reply/', {'text': 'reply', 'comment_id': 1})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your reply has been successfully added')
        self.assertRedirects(response, '/forum/post/1/')
        
    def test_get_edit_reply_view(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get('/forum/post/1/comment/1/reply/edit/')
        self.assertTemplateUsed(response, 'forum/reply_edit_form.html')
        
    def test_post_edit_reply(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/forum/post/1/comment/1/reply/edit/', {'text': 'edited reply'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have successfully edited the reply')
        self.assertRedirects(response, '/forum/post/1/')
        
    def test_reply_remove(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get('/forum/reply/1/remove/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have successfully removed the reply')
        self.assertRedirects(response, '/forum/post/1/')
        
    def test_comment_remove(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get('/forum/comment/1/remove/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have successfully removed the comment')
        self.assertRedirects(response, '/forum/post/1/')
        
    def test_comment_approve(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get('/forum/comment/1/approve/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have successfully approved the comment')
        self.assertRedirects(response, '/forum/post/1/')
        
    def test_get_comment_update_view(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get('/forum/comment/1/edit/')
        self.assertTemplateUsed(response, 'forum/comment_edit_form.html')
        
    def test_post_comment_update(self):
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.post('/forum/comment/1/edit/', {'text': 'edited comment'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have successfully edited the comment')
        self.assertRedirects(response, '/forum/post/1/')
